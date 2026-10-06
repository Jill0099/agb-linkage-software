"""Create and link a tiny synthetic raster; no actual firm or upstream data."""

import argparse
import json
import shutil
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from agb_linkage.config import load_config
from agb_linkage.pipeline import run_extraction


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    raster_path = args.out_dir / "AGB_2020.tif"
    if raster_path.exists():
        raise FileExistsError("Demo output already exists; select a fresh directory")
    with rasterio.open(
        raster_path,
        "w",
        driver="GTiff",
        height=5,
        width=5,
        count=1,
        dtype="uint16",
        crs="EPSG:32650",
        nodata=0,
        transform=from_origin(500000, 3400000, 30, 30),
    ) as ds:
        ds.write(np.arange(25, dtype="uint16").reshape(5, 5), 1)
    example_dir = Path(__file__).parent
    points = args.out_dir / "locations.csv"
    shutil.copyfile(example_dir / "synthetic_locations.csv", points)
    cfg = load_config(example_dir / "synthetic_config.yaml")
    output = args.out_dir / "linked.csv"
    manifest = run_extraction(points, args.out_dir, output, cfg)
    print(json.dumps({"output": str(output), "manifest": str(manifest)}))


if __name__ == "__main__":
    main()
