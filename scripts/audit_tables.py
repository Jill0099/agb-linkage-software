"""Audit local candidate tables without exporting addresses or coordinates.

Paths and hashes go to the caller-selected audit directory. Keep that directory
private when auditing restricted inputs. Aggregate figures are descriptive file
checks, not ecological or geocoding validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AGB_FIELDS = ("agb_px", "agb_m500", "agb_m1000", "agb_m5000")


def file_hash(path: Path) -> str:
    """Hash an input without changing it."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def firm_codes(values: pd.Series) -> pd.Series:
    """Normalise numeric stock identifiers while preserving leading zeros."""
    codes = values.astype("string").str.strip()
    codes = codes.str.replace(r"^(\d+)\.0$", r"\1", regex=True)
    if codes.isna().any() or not codes.str.fullmatch(r"\d{1,6}").all():
        raise ValueError("Stock codes must be nonmissing numeric identifiers.")
    return codes.str.zfill(6)


def key_frame(frame: pd.DataFrame, code_column: str) -> pd.DataFrame:
    """Build explicit stock-code/year keys and fail on invalid years."""
    result = frame.copy()
    result["firm_key"] = firm_codes(result[code_column])
    years = pd.to_numeric(result["year"], errors="raise")
    if years.isna().any() or not np.equal(years, np.floor(years)).all():
        raise ValueError("Years must be nonmissing integers.")
    result["year"] = years.astype(int)
    return result


def counts(frame: pd.DataFrame) -> dict[str, Any]:
    """Return a population description and duplicate-key diagnostic."""
    return {
        "rows": len(frame),
        "firms": int(frame["firm_key"].nunique()),
        "years": sorted(int(v) for v in frame["year"].unique()),
        "duplicate_key_rows": int(frame.duplicated(["firm_key", "year"]).sum()),
        "rows_by_year": {
            str(k): int(v) for k, v in frame.groupby("year").size().items()
        },
    }


def describe_stat(values: pd.Series) -> dict[str, Any]:
    """Describe stored values without assigning unverified physical units."""
    numeric = pd.to_numeric(values, errors="raise")
    finite = numeric[np.isfinite(numeric)]
    result: dict[str, Any] = {
        "nonmissing": int(numeric.notna().sum()),
        "nonfinite_nonmissing": int((numeric.notna() & ~np.isfinite(numeric)).sum()),
        "zero_rows": int(numeric.eq(0).sum()),
        "negative_rows": int(numeric.lt(0).sum()),
        "above_1500_stored_units": int(numeric.gt(1500).sum()),
    }
    if not finite.empty:
        result["quantiles"] = {
            str(q): float(v)
            for q, v in finite.quantile([0, 0.25, 0.5, 0.75, 0.9, 0.99, 1]).items()
        }
    return result


def rank_statistics(left: pd.Series, right: pd.Series) -> dict[str, Any]:
    """Rank only paired finite observations and report the denominator."""
    pair = pd.concat([left, right], axis=1).apply(pd.to_numeric, errors="raise")
    pair = pair.replace([np.inf, -np.inf], np.nan).dropna()
    if pair.empty:
        return {
            "paired_finite_rows": 0,
            "absolute_rank_shift_above_10_percentile_points_rows": 0,
            "share": None,
            "median_absolute_rank_shift_percentile_points": None,
            "spearman_with_m1000": None,
        }
    ranks = pair.rank(pct=True, method="average")
    shifts = (ranks.iloc[:, 0] - ranks.iloc[:, 1]).abs()
    correlation = pair.iloc[:, 0].corr(pair.iloc[:, 1], method="spearman")
    return {
        "paired_finite_rows": len(pair),
        "absolute_rank_shift_above_10_percentile_points_rows": int(
            shifts.gt(0.1).sum()
        ),
        "share": float(shifts.gt(0.1).mean()),
        "median_absolute_rank_shift_percentile_points": float(shifts.median() * 100),
        "spearman_with_m1000": float(correlation) if np.isfinite(correlation) else None,
    }


def build_audit(
    coordinates_path: Path,
    rebuilt_path: Path,
    legacy_path: Path | None = None,
    addresses_path: Path | None = None,
) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame]:
    """Compute joins and statistics without exporting record-level tables."""
    coords = key_frame(
        pd.read_csv(coordinates_path, dtype={"股票代码": str}), "股票代码"
    )
    rebuilt = key_frame(pd.read_csv(rebuilt_path, dtype={"stkcd": str}), "stkcd")
    if coords.duplicated(["firm_key", "year"]).any():
        raise ValueError("Coordinate table has duplicate firm-year keys.")
    if rebuilt.duplicated(["firm_key", "year"]).any():
        raise ValueError("Rebuilt table has duplicate firm-year keys.")
    for frame, columns in ((coords, ("经度", "纬度")), (rebuilt, ("lon", "lat"))):
        for column in columns:
            frame[column] = pd.to_numeric(frame[column], errors="raise")
            if not np.isfinite(frame[column]).all():
                raise ValueError(
                    "Coordinate columns must contain finite numeric values."
                )
    paths = {"coordinates": coordinates_path, "rebuilt": rebuilt_path}
    report: dict[str, Any] = {
        "scope": "Stored-table audit; not raster, CRS, geocoding or rights validation",
        "coordinates": counts(coords),
        "rebuilt": counts(rebuilt),
        "agb": {name: describe_stat(rebuilt[name]) for name in AGB_FIELDS},
        "coordinate_precision_levels": {
            str(k): int(v)
            for k, v in coords["匹配级别"].fillna("missing").value_counts().items()
        },
    }
    report["window_count_values"] = {
        name: sorted(float(v) for v in rebuilt[name].dropna().unique())
        for name in ("agb_n500", "agb_n1000", "agb_n5000")
    }
    merged = rebuilt.merge(
        coords[["firm_key", "year", "经度", "纬度", "匹配级别"]],
        on=["firm_key", "year"],
        how="left",
        validate="one_to_one",
        indicator=True,
    )
    matched = merged["_merge"].eq("both")
    delta_lon = (merged.loc[matched, "lon"] - merged.loc[matched, "经度"]).abs()
    delta_lat = (merged.loc[matched, "lat"] - merged.loc[matched, "纬度"]).abs()
    report["coordinate_lineage_join"] = {
        "matched_keys": int(matched.sum()),
        "unmatched_keys": int((~matched).sum()),
        "changed_coordinate_rows_above_1e_minus_7_degrees": int(
            (delta_lon.gt(1e-7) | delta_lat.gt(1e-7)).sum()
        ),
        "maximum_lon_difference_degrees": float(delta_lon.max())
        if matched.any()
        else None,
        "maximum_lat_difference_degrees": float(delta_lat.max())
        if matched.any()
        else None,
        "interpretation": "Equal coordinates demonstrate lineage, not correct CRS.",
    }
    report["rebuilt_precision_levels"] = {
        str(k): int(v)
        for k, v in merged.loc[matched, "匹配级别"]
        .fillna("missing")
        .value_counts()
        .items()
    }
    xy = coords[["firm_key", "经度", "纬度"]].drop_duplicates()
    locations_per_firm = xy.groupby("firm_key").size()
    report["location_history"] = {
        "firms_with_multiple_stored_coordinate_pairs": int(
            locations_per_firm.gt(1).sum()
        ),
        "firms_with_one_stored_coordinate_pair": int(locations_per_firm.eq(1).sum()),
        "interpretation": (
            "Stored coordinate changes are not independently verified relocations."
        ),
    }
    agb_numeric = rebuilt[list(AGB_FIELDS)].apply(pd.to_numeric, errors="raise")
    matrix = agb_numeric.replace([np.inf, -np.inf], np.nan).corr(method="spearman")
    report["stored_window_spearman_correlations"] = json.loads(matrix.to_json())
    sensitivity: dict[str, Any] = {}
    for name in ("agb_m500", "agb_m5000"):
        sensitivity[name] = rank_statistics(rebuilt[name], rebuilt["agb_m1000"])
        sensitivity[name]["interpretation"] = (
            "Historical pixel squares; not verified physical-radius sensitivity."
        )
    report["stored_window_rank_sensitivity"] = sensitivity
    yearly_sensitivity: dict[str, Any] = {}
    for year, subset in rebuilt.groupby("year"):
        yearly_sensitivity[str(year)] = {
            name: rank_statistics(subset[name], subset["agb_m1000"])
            for name in ("agb_m500", "agb_m5000")
        }
    report["within_year_stored_window_sensitivity"] = yearly_sensitivity
    if addresses_path is not None:
        paths["addresses"] = addresses_path
        source = key_frame(
            pd.read_excel(addresses_path, dtype={"股票代码": str}), "股票代码"
        )
        report["address_source"] = counts(source)
    if legacy_path is not None:
        paths["legacy"] = legacy_path
        legacy = key_frame(
            pd.read_csv(legacy_path, dtype={"股票代码": str}), "股票代码"
        )
        report["legacy"] = counts(legacy)
        report["legacy"]["point_values"] = describe_stat(legacy["AGB_value"])
        common = rebuilt.merge(
            legacy[["firm_key", "year", "AGB_value"]],
            on=["firm_key", "year"],
            how="left",
            validate="one_to_one",
        )
        comparable = common["AGB_value"].notna() & common["agb_px"].notna()
        differences = (
            common.loc[comparable, "AGB_value"] - common.loc[comparable, "agb_px"]
        ).abs()
        report["legacy_comparison"] = {
            "comparable_nonmissing_point_rows": int(comparable.sum()),
            "point_differences_above_0_001": int(differences.gt(0.001).sum()),
            "rebuilt_zero_with_legacy_missing": int(
                (common["agb_px"].eq(0) & common["AGB_value"].isna()).sum()
            ),
        }
    report["inputs"] = {
        key: {
            "path": str(path.resolve()),
            "sha256": file_hash(path),
            "bytes": path.stat().st_size,
        }
        for key, path in paths.items()
    }
    return report, coords, rebuilt


def write_figures(
    coords: pd.DataFrame, rebuilt: pd.DataFrame, output_dir: Path
) -> None:
    """Save standalone aggregate figures with explicit scope labels."""
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {"font.size": 10, "axes.spines.top": False, "axes.spines.right": False}
    )
    coverage = pd.DataFrame(
        {
            "Geocoded office records": coords.groupby("year").size(),
            "Rebuilt candidate": rebuilt.groupby("year").size(),
        }
    ).fillna(0)
    fig, ax = plt.subplots(figsize=(9, 4.3), layout="constrained")
    coverage.plot.bar(ax=ax, color=["#718096", "#187d8c"], width=0.82)
    ax.set(
        xlabel="Year",
        ylabel="Stored firm-year records",
        title="Source coverage and rebuilt candidate population",
    )
    ax.legend(frameon=False)
    for extension in ("png", "pdf"):
        fig.savefig(output_dir / f"coverage.{extension}", dpi=200)
    plt.close(fig)
    shares = rebuilt[list(AGB_FIELDS)].eq(0).mean() * 100
    fig, ax = plt.subplots(figsize=(7.5, 4.2), layout="constrained")
    bars = ax.bar(
        ["Point", "35 × 35 cells", "67 × 67 cells", "335 × 335 cells"],
        shares,
        color="#187d8c",
    )
    ax.bar_label(bars, fmt="%.2f%%", padding=4)
    ax.set(
        ylim=(0, 100),
        ylabel="Rows with stored numeric zero (%)",
        title="Zeros in the historical extraction specifications",
    )
    ax.set_xlabel(
        "File contents only; zero semantics and physical window sizes "
        "remain unverified.",
        fontsize=8,
        labelpad=12,
    )
    for extension in ("png", "pdf"):
        fig.savefig(output_dir / f"zero_shares.{extension}", dpi=200)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coordinates", type=Path, required=True)
    parser.add_argument("--rebuilt", type=Path, required=True)
    parser.add_argument("--legacy", type=Path)
    parser.add_argument("--addresses", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report, coords, rebuilt = build_audit(
        args.coordinates, args.rebuilt, args.legacy, args.addresses
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = args.output_dir / "table_audit.json"
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    )
    write_figures(coords, rebuilt, args.output_dir / "figures")
    print(f"Aggregate audit written to {target}; no record-level data exported.")


if __name__ == "__main__":
    main()
