"""Immutable extraction settings with explicit coordinate and mask declarations."""

from dataclasses import asdict, dataclass
from functools import lru_cache
from math import isclose, isfinite, pi
from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pyproj import CRS
from pyproj.exceptions import CRSError


@dataclass(frozen=True)
class ExtractionConfig:
    coordinate_crs: str
    mode: str = "legacy_pixel_square"
    radii_m: tuple[float, ...] = (500.0, 1000.0, 5000.0)
    mask_policy: str = "respect"
    zero_policy: str = "include"
    id_column: str = "location_id"
    year_column: str = "year"
    x_column: str = "x"
    y_column: str = "y"
    raster_template: str = "AGB_{year}.tif"
    band: int = 1
    missing_year_policy: str = "error"
    apply_scale: bool = False
    hash_rasters: bool = False
    max_window_pixels: int = 4_000_000
    source_name: str = "unspecified"
    source_version: str = "unverified"
    source_doi: str = "unverified"

    def __post_init__(self) -> None:
        validate_crs(self.coordinate_crs)
        choices = {
            "mode": {"legacy_pixel_square", "metric_circle"},
            "mask_policy": {"respect", "include_zero_nodata"},
            "zero_policy": {"include", "exclude"},
            "missing_year_policy": {"error", "record"},
        }
        for field, allowed in choices.items():
            if getattr(self, field) not in allowed:
                raise ValueError(f"Invalid {field}: {getattr(self, field)!r}")
        radii = tuple(float(r) for r in self.radii_m)
        if not radii or any(not isfinite(r) or r <= 0 for r in radii):
            raise ValueError("radii_m must contain positive finite radii")
        if len(set(radii)) != len(radii):
            raise ValueError("radii_m must be unique")
        if self.mode == "metric_circle" and max(radii) > 100_000:
            raise ValueError("metric_circle currently supports radii up to 100 km")
        object.__setattr__(self, "radii_m", radii)
        for field in ("band", "max_window_pixels"):
            value = getattr(self, field)
            if type(value) is not int or value < 1:
                raise ValueError(f"{field} must be a positive integer")
        for field in ("apply_scale", "hash_rasters"):
            if type(getattr(self, field)) is not bool:
                raise ValueError(f"{field} must be a boolean")
        columns = (self.id_column, self.year_column, self.x_column, self.y_column)
        if len(set(columns)) != 4 or any(not col.strip() for col in columns):
            raise ValueError("Input column names must be nonempty and distinct")
        try:
            self.raster_template.format(year=2020)
        except (KeyError, ValueError) as exc:
            raise ValueError("Invalid raster_template; use {year}") from exc
        if "{year}" not in self.raster_template:
            raise ValueError("raster_template must contain {year}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@lru_cache(maxsize=32)
def validate_crs(value: str) -> CRS:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("An explicit coordinate CRS is required")
    lowered = value.lower().replace("-", "").replace("_", "")
    if any(marker in lowered for marker in ("gcj", "bd09", "unresolved")):
        raise ValueError(
            "Unresolved coordinate CRS: convert GCJ-02/BD-09 with a verified "
            "procedure before extraction; do not relabel coordinates as WGS84"
        )
    try:
        crs = CRS.from_user_input(value)
    except CRSError as exc:
        raise ValueError(f"Invalid coordinate CRS: {value!r}") from exc
    if not (crs.is_geographic or crs.is_projected):
        raise ValueError("coordinate CRS must be geographic or projected")
    if crs.is_geographic and any(
        not isclose(axis.unit_conversion_factor, pi / 180, rel_tol=1e-10)
        for axis in crs.axis_info[:2]
    ):
        raise ValueError("Geographic coordinate CRS must use degree units")
    return crs


def load_config(
    path: Path, overrides: dict[str, Any] | None = None
) -> ExtractionConfig:
    try:
        data = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
    except Exception as exc:
        raise ValueError(f"Cannot read extraction configuration: {path}") from exc
    if not isinstance(data, dict):
        raise ValueError("Configuration must be a mapping")
    allowed = set(ExtractionConfig.__dataclass_fields__)
    unknown = set(data) - allowed
    if unknown:
        raise ValueError(f"Unknown configuration fields: {sorted(unknown)}")
    data.update(overrides or {})
    try:
        return ExtractionConfig(**data)
    except TypeError as exc:
        raise ValueError(f"Invalid extraction configuration: {exc}") from exc
