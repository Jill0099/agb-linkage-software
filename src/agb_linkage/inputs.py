"""Validate location-year inputs without coercing identifiers to numbers."""

import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path

from .config import ExtractionConfig, validate_crs


@dataclass(frozen=True)
class LocationYear:
    location_id: str
    year: int
    x: float
    y: float


def validate_coordinates(x: float, y: float, coordinate_crs: str) -> None:
    if not (math.isfinite(x) and math.isfinite(y)):
        raise ValueError("Coordinates must be finite")
    crs = validate_crs(coordinate_crs)
    if crs.is_geographic:
        if not (-180 <= x <= 180):
            raise ValueError("Geographic longitude must be between -180 and 180")
        if not (-90 <= y <= 90):
            raise ValueError("Geographic latitude must be between -90 and 90")


def read_locations(path: Path, cfg: ExtractionConfig) -> list[LocationYear]:
    records: list[LocationYear] = []
    seen: set[tuple[str, int]] = set()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        expected = {cfg.id_column, cfg.year_column, cfg.x_column, cfg.y_column}
        if len(set(columns)) != len(columns) or not expected.issubset(columns):
            raise ValueError(f"Missing or duplicate CSV columns; required {expected}")
        for line, row in enumerate(reader, start=2):
            if None in row or any(row[col] is None for col in expected):
                raise ValueError(f"Malformed CSV row {line}")
            identifier = row[cfg.id_column].strip()
            if not identifier:
                raise ValueError(f"Empty location ID at row {line}")
            year_text = row[cfg.year_column].strip()
            if not re.fullmatch(r"\d{4}", year_text):
                raise ValueError(f"Expected integer year at row {line}")
            year = int(year_text)
            if not 1900 <= year <= 2100:
                raise ValueError(f"Unsupported year range at row {line}")
            key = (identifier, year)
            if key in seen:
                raise ValueError(f"Duplicate location-year key at row {line}: {key}")
            try:
                x, y = float(row[cfg.x_column]), float(row[cfg.y_column])
            except ValueError as exc:
                raise ValueError(f"Invalid numeric coordinates at row {line}") from exc
            validate_coordinates(x, y, cfg.coordinate_crs)
            seen.add(key)
            records.append(LocationYear(identifier, year, x, y))
    if not records:
        raise ValueError("Location-year CSV is empty")
    return sorted(records, key=lambda record: (record.year, record.location_id))
