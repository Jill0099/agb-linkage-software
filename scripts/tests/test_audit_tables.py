"""Check key scientific audit claims against small hand-defined inputs."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "audit_tables.py"
SPEC = importlib.util.spec_from_file_location("audit_tables", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def write_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    coords = pd.DataFrame(
        {
            "股票代码": ["000001", "000002", "000003"],
            "year": [2020] * 3,
            "经度": [100.0, 101.0, 102.0],
            "纬度": [30.0] * 3,
            "匹配级别": ["门牌号", "市", "未知"],
        }
    )
    rebuilt = pd.DataFrame(
        {
            "stkcd": ["000001", "000002", "000003"],
            "year": [2020] * 3,
            "lon": [100.0, 101.0, 102.5],
            "lat": [30.0] * 3,
            "agb_px": [0.0, 10.0, 20.0],
            "agb_m500": [3.0, 2.0, 1.0],
            "agb_m1000": [1.0, 2.0, 3.0],
            "agb_m5000": [2.0, 1.0, 3.0],
            "agb_n500": [1225] * 3,
            "agb_n1000": [4489] * 3,
            "agb_n5000": [112225] * 3,
        }
    )
    legacy = pd.DataFrame(
        {
            "股票代码": ["000001", "000002", "000003"],
            "year": [2020] * 3,
            "AGB_value": [None, 10.0, 22.0],
        }
    )
    paths = (tmp_path / "coords.csv", tmp_path / "rebuilt.csv", tmp_path / "legacy.csv")
    for table, path in zip((coords, rebuilt, legacy), paths, strict=True):
        table.to_csv(path, index=False)
    return paths


def test_lineage_missingness_and_rank_audit(tmp_path: Path) -> None:
    coords, rebuilt, legacy = write_inputs(tmp_path)
    result, _, _ = audit.build_audit(coords, rebuilt, legacy)
    assert result["coordinate_lineage_join"]["matched_keys"] == 3
    assert (
        result["coordinate_lineage_join"][
            "changed_coordinate_rows_above_1e_minus_7_degrees"
        ]
        == 1
    )
    assert result["legacy_comparison"]["rebuilt_zero_with_legacy_missing"] == 1
    assert result["legacy_comparison"]["point_differences_above_0_001"] == 1
    assert (
        result["stored_window_spearman_correlations"]["agb_m1000"]["agb_m500"] == -1.0
    )
    assert result["stored_window_rank_sensitivity"]["agb_m500"][
        "share"
    ] == pytest.approx(2 / 3)


def test_duplicate_keys_fail_instead_of_expanding_join(tmp_path: Path) -> None:
    coords, rebuilt, _ = write_inputs(tmp_path)
    frame = pd.read_csv(coords, dtype={"股票代码": str})
    pd.concat([frame, frame.iloc[[0]]]).to_csv(coords, index=False)
    with pytest.raises(ValueError, match="duplicate"):
        audit.build_audit(coords, rebuilt)


@pytest.mark.parametrize("identifier", [None, "ABC123", "0000010"])
def test_invalid_identifiers_are_rejected(identifier: str | None) -> None:
    with pytest.raises(ValueError, match="Stock codes"):
        audit.firm_codes(pd.Series([identifier]))


def test_missing_coordinate_is_not_reported_unchanged(tmp_path: Path) -> None:
    coords, rebuilt, _ = write_inputs(tmp_path)
    frame = pd.read_csv(rebuilt, dtype={"stkcd": str})
    frame.loc[1, "lon"] = float("nan")
    frame.to_csv(rebuilt, index=False)
    with pytest.raises(ValueError, match="finite"):
        audit.build_audit(coords, rebuilt)


def test_rank_comparison_uses_only_paired_finite_values() -> None:
    result = audit.rank_statistics(
        pd.Series([1.0, 2.0, None, float("inf")]),
        pd.Series([2.0, 1.0, 3.0, 4.0]),
    )
    assert result["paired_finite_rows"] == 2
    assert result["share"] == 1.0
    assert result["spearman_with_m1000"] == pytest.approx(-1.0)
