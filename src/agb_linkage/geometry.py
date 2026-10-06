"""Registered footprint strategies; selection is separate from data validity."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from math import ceil, cos, degrees, floor, isfinite, radians

import numpy as np
import rasterio
from pyproj import Geod, Transformer
from rasterio.warp import transform_bounds
from rasterio.windows import Window

from .config import validate_crs

GEOD = Geod(ellps="WGS84")
LEGACY_METERS_PER_DEGREE = 111000.0


@lru_cache(maxsize=32)
def coordinate_transformer(source: str, destination: str) -> Transformer:
    return Transformer.from_crs(
        source, destination, always_xy=True, allow_ballpark=False
    )


@dataclass(frozen=True)
class Selection:
    window: Window
    eligible: np.ndarray
    half_cells: int | None
    requested_square_count: int | None
    extent_clipped: bool
    geometry_rule: str


Strategy = Callable[[rasterio.io.DatasetReader, float, float, float, int], Selection]
STRATEGIES: dict[str, Strategy] = {}


def register_strategy(name: str) -> Callable[[Strategy], Strategy]:
    def register(function: Strategy) -> Strategy:
        if name in STRATEGIES:
            raise ValueError(f"Duplicate extraction strategy: {name}")
        STRATEGIES[name] = function
        return function

    return register


def get_strategy(name: str) -> Strategy:
    try:
        return STRATEGIES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown extraction strategy: {name}") from exc


def bounded_window(
    ds: rasterio.io.DatasetReader,
    r0: int,
    r1: int,
    c0: int,
    c1: int,
    max_pixels: int,
) -> tuple[Window, bool]:
    clipped = r0 < 0 or c0 < 0 or r1 > ds.height or c1 > ds.width
    r0, r1 = max(0, r0), min(ds.height, r1)
    c0, c1 = max(0, c0), min(ds.width, c1)
    if (r1 - r0) * (c1 - c0) > max_pixels:
        raise ValueError("Extraction exceeds the configured window pixel limit")
    return Window(c0, r0, max(0, c1 - c0), max(0, r1 - r0)), clipped


@register_strategy("legacy_pixel_square")
def legacy_square(
    ds: rasterio.io.DatasetReader, x: float, y: float, radius: float, max_pixels: int
) -> Selection:
    if not ds.crs.is_geographic:
        raise ValueError("legacy_pixel_square requires a geographic raster CRS")
    validate_crs(ds.crs.to_string())
    if ds.transform.a <= 0 or ds.transform.e >= 0:
        raise ValueError("legacy_pixel_square requires a north-up geographic grid")
    if ds.transform.b != 0 or ds.transform.d != 0:
        raise ValueError("legacy_pixel_square requires an unrotated geographic grid")
    row, col = ds.index(x, y)
    half = max(1, int(round(radius / LEGACY_METERS_PER_DEGREE / ds.res[0])))
    window, clipped = bounded_window(
        ds, row - half, row + half + 1, col - half, col + half + 1, max_pixels
    )
    eligible = np.ones((int(window.height), int(window.width)), dtype=bool)
    return Selection(
        window,
        eligible,
        half,
        (2 * half + 1) ** 2,
        clipped,
        "legacy_round_radius_over_111000_over_x_resolution_square",
    )


@register_strategy("metric_circle")
def metric_circle(
    ds: rasterio.io.DatasetReader, x: float, y: float, radius: float, max_pixels: int
) -> Selection:
    """Select centers by WGS84 ellipsoidal distance, after CRS transformation.

    A conservative geographic bounding box limits reads. A 6,300 km lower
    curvature-radius bound and the maximum latitude of that box expand it beyond
    the disk. PROJ densifies its boundary before conversion to the raster CRS;
    a two-pixel margin protects discretization. This implementation deliberately
    rejects pole/dateline-crossing disks and radii above 100 km.
    """
    if radius > 100_000:
        raise ValueError("metric_circle currently supports radii up to 100 km")
    to_geographic = coordinate_transformer(ds.crs.to_string(), "EPSG:4326")
    lon, lat = to_geographic.transform(x, y)
    angular_margin = degrees(radius / 6_300_000.0)
    max_abs_lat = abs(lat) + angular_margin
    if max_abs_lat >= 89:
        raise ValueError("metric_circle does not yet support polar footprints")
    longitude_margin = angular_margin / cos(radians(max_abs_lat))
    if lon - longitude_margin <= -180 or lon + longitude_margin >= 180:
        raise ValueError("metric_circle does not yet support dateline crossings")
    bounds = transform_bounds(
        "EPSG:4326",
        ds.crs,
        lon - longitude_margin,
        lat - angular_margin,
        lon + longitude_margin,
        lat + angular_margin,
        densify_pts=101,
    )
    if not all(isfinite(v) for v in bounds):
        raise ValueError("Cannot transform metric footprint into raster CRS")
    left, bottom, right, top = bounds
    corners = [~ds.transform * (cx, cy) for cx in (left, right) for cy in (bottom, top)]
    cols, rows = zip(*corners, strict=True)
    window, clipped = bounded_window(
        ds,
        floor(min(rows)) - 2,
        ceil(max(rows)) + 2,
        floor(min(cols)) - 2,
        ceil(max(cols)) + 2,
        max_pixels,
    )
    row_grid, col_grid = np.meshgrid(
        np.arange(int(window.row_off), int(window.row_off + window.height)) + 0.5,
        np.arange(int(window.col_off), int(window.col_off + window.width)) + 0.5,
        indexing="ij",
    )
    transform = ds.transform
    xs = transform.c + transform.a * col_grid + transform.b * row_grid
    ys = transform.f + transform.d * col_grid + transform.e * row_grid
    if xs.size == 1:
        longitude, latitude = to_geographic.transform(
            float(xs.flat[0]), float(ys.flat[0])
        )
        _, _, distance = GEOD.inv(lon, lat, longitude, latitude)
        distances = np.full(xs.shape, distance)
    else:
        longitudes, latitudes = to_geographic.transform(xs, ys)
        _, _, distances = GEOD.inv(
            np.full(xs.shape, lon), np.full(xs.shape, lat), longitudes, latitudes
        )
    eligible = np.isfinite(distances) & (distances <= radius)
    return Selection(
        window, eligible, None, None, clipped, "wgs84_geodesic_cell_centers"
    )
