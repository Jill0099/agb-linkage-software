"""Command-line inspection and configurable location-year extraction."""

import argparse
import json
import sys
from pathlib import Path

from .config import ExtractionConfig, load_config
from .metadata import inspect_raster
from .pipeline import run_extraction


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(prog="agb-linkage")
    sub = command.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect-raster", help="Print raster metadata as JSON")
    inspect.add_argument("raster", type=Path)
    inspect.add_argument("--hash", action="store_true", help="Also compute SHA-256")
    extract = sub.add_parser(
        "extract", help="Extract one record per location-year-radius"
    )
    extract.add_argument("--points", type=Path, required=True)
    extract.add_argument("--rasters", type=Path, required=True)
    extract.add_argument("--out", type=Path, required=True)
    extract.add_argument("--config", type=Path)
    extract.add_argument("--coordinate-crs")
    extract.add_argument("--mode", choices=["legacy_pixel_square", "metric_circle"])
    extract.add_argument("--radii-m", type=float, nargs="+")
    extract.add_argument("--mask-policy", choices=["respect", "include_zero_nodata"])
    extract.add_argument("--zero-policy", choices=["include", "exclude"])
    extract.add_argument("--missing-year-policy", choices=["error", "record"])
    extract.add_argument("--hash-rasters", action="store_true", default=None)
    extract.add_argument("--apply-scale", action="store_true", default=None)
    return command


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "inspect-raster":
            print(
                json.dumps(inspect_raster(arguments.raster, arguments.hash), indent=2)
            )
        else:
            names = (
                "coordinate_crs",
                "mode",
                "radii_m",
                "mask_policy",
                "zero_policy",
                "missing_year_policy",
                "hash_rasters",
                "apply_scale",
            )
            overrides = {
                name: getattr(arguments, name)
                for name in names
                if getattr(arguments, name) is not None
            }
            if arguments.config:
                cfg = load_config(arguments.config, overrides)
            else:
                if "coordinate_crs" not in overrides or "mode" not in overrides:
                    raise ValueError(
                        "Explicit --coordinate-crs and --mode are required"
                    )
                cfg = ExtractionConfig(**overrides)
            manifest = run_extraction(
                arguments.points, arguments.rasters, arguments.out, cfg
            )
            print(json.dumps({"output": str(arguments.out), "manifest": str(manifest)}))
    except (OSError, ValueError, TypeError) as exc:
        print(f"agb-linkage: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
