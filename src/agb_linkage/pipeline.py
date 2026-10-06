"""Validated year-matched extraction and atomic output with a run manifest."""

import csv
import json
import os
import platform
import tempfile
from collections import Counter
from dataclasses import asdict
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path

import rasterio

from . import __version__
from .config import ExtractionConfig
from .extraction import SampleResult, extract_point
from .inputs import read_locations
from .metadata import inspect_raster, sha256_file


def run_extraction(
    points: Path,
    rasters: Path,
    output: Path,
    cfg: ExtractionConfig,
) -> Path:
    manifest_path = output.with_suffix(output.suffix + ".manifest.json")
    if (
        output.resolve() == points.resolve()
        or manifest_path.resolve() == points.resolve()
    ):
        raise ValueError("Output must not replace the input")
    if output.exists() or manifest_path.exists():
        raise FileExistsError(
            "Output or manifest already exists; select a new output path"
        )
    records = read_locations(points, cfg)
    year_paths = {
        year: rasters / cfg.raster_template.format(year=year)
        for year in {record.year for record in records}
    }
    if any(output.resolve() == path.resolve() for path in year_paths.values()):
        raise ValueError("Output must not replace a raster input")
    missing = sorted(year for year, path in year_paths.items() if not path.exists())
    if missing and cfg.missing_year_policy == "error":
        raise FileNotFoundError(f"Missing raster years: {missing}")
    metadata = {
        str(year): inspect_raster(path, cfg.hash_rasters)
        for year, path in sorted(year_paths.items())
        if path.exists()
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    statuses: Counter[str] = Counter()
    fields = ["location_id", "year", "raster_name", "mask_policy", "zero_policy"]
    fields += list(SampleResult.__dataclass_fields__)
    temporary: Path | None = None
    temporary_manifest: Path | None = None
    active_year: int | None = None
    ds = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            dir=output.parent,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for record in records:
                raster_path = year_paths[record.year]
                if record.year != active_year:
                    if ds is not None:
                        ds.close()
                    ds = rasterio.open(raster_path) if raster_path.exists() else None
                    active_year = record.year
                for radius in cfg.radii_m:
                    result = (
                        extract_point(ds, record.x, record.y, radius, cfg)
                        if ds is not None
                        else SampleResult(
                            radius, cfg.mode, "none", status="missing_raster"
                        )
                    )
                    writer.writerow(
                        {
                            "location_id": record.location_id,
                            "year": record.year,
                            "raster_name": raster_path.name,
                            "mask_policy": cfg.mask_policy,
                            "zero_policy": cfg.zero_policy,
                            **asdict(result),
                        }
                    )
                    statuses[result.status] += 1
        manifest = {
            "package_version": __version__,
            "created_utc": datetime.now(UTC).isoformat(),
            "input_file": str(points),
            "input_sha256": sha256_file(points),
            "input_rows": len(records),
            "output_file": str(output),
            "output_sha256": sha256_file(temporary),
            "output_rows": sum(statuses.values()),
            "config": cfg.to_dict(),
            "rasters": metadata,
            "missing_raster_years": missing,
            "status_counts": dict(statuses),
            "environment": {
                "python": platform.python_version(),
                **{
                    name: version(name)
                    for name in ("numpy", "rasterio", "pyproj", "omegaconf")
                },
                "gdal": rasterio.__gdal_version__,
            },
            "geometry_notes": {
                "legacy_pixel_square": (
                    "Half-width max(1, round(radius/111000/x_resolution)) cells "
                    "on a geographic grid; not a metric radius."
                ),
                "metric_circle": (
                    "WGS84 ellipsoidal distance from input point to "
                    "raster cell centers."
                ),
                "extent_clipped": (
                    "Candidate window intersects raster extent; "
                    "conservative for metric circles."
                ),
                "outside_extent": (
                    "A center outside the raster is recorded without "
                    "extracting overlapping cells."
                ),
                "center_pixel_raw": (
                    "Raw native-grid cell containing the transformed coordinate; "
                    "reported separately from policy-valid/scaled center_pixel_value."
                ),
                "zero_count": (
                    "Finite, unmasked raw zeros before optional zero exclusion "
                    "and scale/offset."
                ),
            },
            "source_rights": (
                "Not assessed by this extraction; source metadata "
                "is a user declaration."
            ),
        }
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output.parent,
            prefix=f".{manifest_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_manifest = Path(handle.name)
            json.dump(manifest, handle, indent=2, sort_keys=True, allow_nan=False)
            handle.write("\n")
        # Link exclusively, so even a concurrent writer cannot be overwritten.
        os.link(temporary, output)
        try:
            os.link(temporary_manifest, manifest_path)
        except Exception:
            output.unlink()
            raise
    finally:
        if ds is not None:
            ds.close()
        for path in (temporary, temporary_manifest):
            if path is not None:
                path.unlink(missing_ok=True)
    return manifest_path
