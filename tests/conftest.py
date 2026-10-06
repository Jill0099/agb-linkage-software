from pathlib import Path

import numpy as np
import pytest
import rasterio
from rasterio.transform import from_origin


@pytest.fixture
def raster_factory(tmp_path):
    def create(
        values,
        *,
        name="AGB_2020.tif",
        crs="EPSG:4326",
        transform=None,
        nodata=0,
        mask=None,
    ) -> Path:
        data = np.asarray(values, dtype="float32")
        path = tmp_path / name
        transform = transform or from_origin(
            116, 40, 0.00026949458523585647, 0.00026949458523585647
        )
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            height=data.shape[0],
            width=data.shape[1],
            count=1,
            dtype=data.dtype,
            crs=crs,
            transform=transform,
            nodata=nodata,
        ) as ds:
            ds.write(data, 1)
            if mask is not None:
                ds.write_mask(np.asarray(mask, dtype="uint8"))
        return path

    return create
