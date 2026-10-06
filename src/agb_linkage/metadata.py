"""Inspect source metadata without asserting scientific units or source rights."""

import hashlib
import math
from pathlib import Path
from typing import Any

import rasterio


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_raster(path: Path, hash_file: bool = False) -> dict[str, Any]:
    with rasterio.open(path) as ds:
        authority = ds.crs.to_authority() if ds.crs else None
        nodata = ds.nodata
        if nodata is not None and not math.isfinite(nodata):
            nodata = str(nodata)
        result: dict[str, Any] = {
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "driver": ds.driver,
            "width": ds.width,
            "height": ds.height,
            "band_count": ds.count,
            "dtypes": list(ds.dtypes),
            "crs_authority": list(authority) if authority else None,
            "crs_wkt": ds.crs.to_wkt() if ds.crs else None,
            "transform": list(ds.transform)[:6],
            "bounds": list(ds.bounds),
            "resolution": list(ds.res),
            "nodata": nodata,
            "mask_flags": [
                [flag.name for flag in flags] for flags in ds.mask_flag_enums
            ],
            "scales": list(ds.scales),
            "offsets": list(ds.offsets),
            "band_units": list(ds.units),
            "band_descriptions": list(ds.descriptions),
            "value_interpretation": (
                "raw band values unless apply_scale is explicitly enabled"
            ),
        }
    if hash_file:
        result["sha256"] = sha256_file(path)
    return result
