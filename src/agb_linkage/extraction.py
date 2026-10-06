"""Raster extraction with explicit geometry, GDAL mask and raw-zero semantics."""

from dataclasses import dataclass
from math import isfinite

import numpy as np
import rasterio
from rasterio.enums import MaskFlags

from .config import ExtractionConfig
from .geometry import coordinate_transformer, get_strategy
from .inputs import validate_coordinates


@dataclass(frozen=True)
class SampleResult:
    radius_m: float
    mode: str
    geometry_rule: str
    eligible_count: int = 0
    valid_count: int = 0
    masked_count: int = 0
    nonfinite_count: int = 0
    zero_count: int = 0
    zero_excluded_count: int = 0
    mean: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    std_population: float | None = None
    center_pixel_raw: float | None = None
    center_pixel_value: float | None = None
    center_pixel_valid: bool = False
    half_cells: int | None = None
    requested_square_count: int | None = None
    window_width: int = 0
    window_height: int = 0
    extent_clipped: bool = False
    status: str = "ok"


def extract_point(
    ds: rasterio.io.DatasetReader,
    x: float,
    y: float,
    radius_m: float,
    cfg: ExtractionConfig,
) -> SampleResult:
    validate_coordinates(x, y, cfg.coordinate_crs)
    if ds.crs is None:
        raise ValueError("Raster CRS is missing; explicit metadata is required")
    if not 1 <= cfg.band <= ds.count:
        raise ValueError("Requested raster band does not exist")
    if not isfinite(radius_m) or radius_m <= 0:
        raise ValueError("Extraction radius must be positive and finite")
    transformer = coordinate_transformer(cfg.coordinate_crs, ds.crs.to_string())
    raster_x, raster_y = transformer.transform(x, y)
    if not (isfinite(raster_x) and isfinite(raster_y)):
        raise ValueError("Coordinate transformation returned nonfinite values")
    row, col = ds.index(raster_x, raster_y)
    if not (0 <= row < ds.height and 0 <= col < ds.width):
        return SampleResult(radius_m, cfg.mode, "none", status="outside_extent")
    selection = get_strategy(cfg.mode)(
        ds, raster_x, raster_y, radius_m, cfg.max_window_pixels
    )
    raw = ds.read(cfg.band, window=selection.window, masked=False).astype("float64")
    mask = ds.read_masks(cfg.band, window=selection.window) != 0
    flags = ds.mask_flag_enums[cfg.band - 1]
    if (
        cfg.mask_policy == "include_zero_nodata"
        and ds.nodatavals[cfg.band - 1] == 0
        and MaskFlags.nodata in flags
        and MaskFlags.per_dataset not in flags
        and MaskFlags.alpha not in flags
    ):
        # Ignore only the nodata-derived zero mask, preserving independent masks.
        mask = np.ones(raw.shape, dtype=bool)
    eligible = selection.eligible
    finite = np.isfinite(raw)
    valid = eligible & mask & finite
    zero_count = int(np.count_nonzero(valid & (raw == 0)))
    zero_excluded = zero_count if cfg.zero_policy == "exclude" else 0
    if cfg.zero_policy == "exclude":
        valid &= raw != 0
    values = raw[valid]
    center_row = int(row - selection.window.row_off)
    center_col = int(col - selection.window.col_off)
    center_raw = raw[center_row, center_col]
    center_valid = bool(mask[center_row, center_col] and isfinite(center_raw))
    if cfg.zero_policy == "exclude" and center_raw == 0:
        center_valid = False
    center_value = float(center_raw) if center_valid else None
    if cfg.apply_scale:
        values = values * ds.scales[cfg.band - 1] + ds.offsets[cfg.band - 1]
        if center_value is not None:
            center_value = (
                center_value * ds.scales[cfg.band - 1] + ds.offsets[cfg.band - 1]
            )
        if not np.all(np.isfinite(values)) or (
            center_value is not None and not isfinite(center_value)
        ):
            raise ValueError("Raster scale/offset produces nonfinite values")
    return SampleResult(
        radius_m=radius_m,
        mode=cfg.mode,
        geometry_rule=selection.geometry_rule,
        eligible_count=int(np.count_nonzero(eligible)),
        valid_count=int(values.size),
        masked_count=int(np.count_nonzero(eligible & ~mask)),
        nonfinite_count=int(np.count_nonzero(eligible & mask & ~finite)),
        zero_count=zero_count,
        zero_excluded_count=zero_excluded,
        mean=float(values.mean()) if values.size else None,
        minimum=float(values.min()) if values.size else None,
        maximum=float(values.max()) if values.size else None,
        std_population=float(values.std()) if values.size else None,
        center_pixel_raw=float(center_raw) if isfinite(center_raw) else None,
        center_pixel_value=center_value,
        center_pixel_valid=center_valid,
        half_cells=selection.half_cells,
        requested_square_count=selection.requested_square_count,
        window_width=int(selection.window.width),
        window_height=int(selection.window.height),
        extent_clipped=selection.extent_clipped,
        status="ok" if values.size else "no_valid_cells",
    )
