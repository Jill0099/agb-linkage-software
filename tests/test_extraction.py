import numpy as np
import pytest
import rasterio
from pyproj import Transformer
from rasterio.transform import from_origin

from agb_linkage.config import ExtractionConfig
from agb_linkage.extraction import extract_point


def config(**kwargs):
    return ExtractionConfig(coordinate_crs="EPSG:4326", **kwargs)


def test_legacy_square_keeps_declared_zero_nodata(raster_factory):
    path = raster_factory([[0, 2, 4], [6, 8, 10], [12, 14, 16]])
    cfg = config(mode="legacy_pixel_square", mask_policy="include_zero_nodata")
    with rasterio.open(path) as ds:
        result = extract_point(ds, *ds.xy(1, 1), 30, cfg)
    assert result.eligible_count == result.valid_count == 9
    assert result.mean == pytest.approx(8)
    assert result.zero_count == 1
    assert result.half_cells == 1
    assert result.status == "ok"


def test_respect_mask_distinguishes_zero_nodata(raster_factory):
    path = raster_factory([[0, 2, 4], [6, 8, 10], [12, 14, 16]])
    with rasterio.open(path) as ds:
        result = extract_point(ds, *ds.xy(1, 1), 30, config())
    assert result.eligible_count == 9
    assert result.valid_count == 8
    assert result.mean == pytest.approx(9)
    assert result.masked_count == 1


def test_true_zero_survives_negative_nodata(raster_factory):
    path = raster_factory([[0, -9999, 4], [6, 8, 10], [12, 14, 16]], nodata=-9999)
    cfg = config(mask_policy="include_zero_nodata")
    with rasterio.open(path) as ds:
        result = extract_point(ds, *ds.xy(1, 1), 30, cfg)
    assert result.valid_count == 8
    assert result.zero_count == 1
    assert result.mean == pytest.approx(8.75)


def test_independent_mask_is_honoured_when_zero_nodata_included(raster_factory):
    path = raster_factory(
        [[0, 2, 4], [6, 8, 10], [12, 14, 16]],
        mask=[[255, 0, 255], [255, 255, 255], [255, 255, 255]],
    )
    with rasterio.open(path) as ds:
        result = extract_point(
            ds, *ds.xy(1, 1), 30, config(mask_policy="include_zero_nodata")
        )
    assert result.valid_count == 8
    assert result.zero_count == 1
    assert result.mean == pytest.approx(8.75)


def test_zero_exclusion_and_nonfinite_values_are_counted(raster_factory):
    path = raster_factory([[0, np.nan, 4], [6, 8, 10], [12, 14, 16]], nodata=None)
    with rasterio.open(path) as ds:
        result = extract_point(ds, *ds.xy(1, 1), 30, config(zero_policy="exclude"))
    assert result.eligible_count == 9
    assert result.valid_count == 7
    assert result.zero_count == 1
    assert result.zero_excluded_count == 1
    assert result.nonfinite_count == 1


def test_square_edges_clip_without_padding(raster_factory):
    path = raster_factory(np.full((3, 3), 7))
    with rasterio.open(path) as ds:
        result = extract_point(ds, *ds.xy(0, 0), 30, config())
    assert result.eligible_count == 4
    assert result.requested_square_count == 9
    assert result.extent_clipped
    assert result.mean == 7


def test_legacy_fixed_cell_counts_and_bankers_rounding(raster_factory):
    path = raster_factory(np.ones((400, 400)))
    with rasterio.open(path) as ds:
        for radius, expected in [
            (1, 9),
            (15, 9),
            (45, 25),
            (500, 1225),
            (1000, 4489),
            (5000, 112225),
        ]:
            result = extract_point(ds, *ds.xy(200, 200), radius, config())
            assert result.eligible_count == expected


def test_metric_circle_is_geodesic_and_different_from_square(raster_factory):
    path = raster_factory(
        np.arange(25).reshape(5, 5),
        nodata=None,
        crs="EPSG:32650",
        transform=from_origin(500000, 3400000, 30, 30),
    )
    with rasterio.open(path) as ds:
        result = extract_point(
            ds,
            500075,
            3399925,
            31,
            ExtractionConfig(coordinate_crs="EPSG:32650", mode="metric_circle"),
        )
    assert result.eligible_count == 5
    assert result.mean == pytest.approx(12)
    assert result.half_cells is None
    assert result.geometry_rule == "wgs84_geodesic_cell_centers"


def test_input_crs_transform_preserves_result(raster_factory):
    path = raster_factory(
        np.arange(25).reshape(5, 5),
        nodata=None,
        crs="EPSG:32650",
        transform=from_origin(500000, 3400000, 30, 30),
    )
    lon, lat = Transformer.from_crs(32650, 4326, always_xy=True).transform(
        500075, 3399925
    )
    with rasterio.open(path) as ds:
        metric = extract_point(
            ds,
            500075,
            3399925,
            31,
            ExtractionConfig(coordinate_crs="EPSG:32650", mode="metric_circle"),
        )
        geographic = extract_point(
            ds,
            lon,
            lat,
            31,
            ExtractionConfig(coordinate_crs="EPSG:4326", mode="metric_circle"),
        )
    assert geographic.mean == metric.mean
    assert geographic.eligible_count == metric.eligible_count


def test_geographic_raster_metric_circle(raster_factory):
    path = raster_factory(
        np.arange(25).reshape(5, 5),
        crs="EPSG:4326",
        transform=from_origin(116, 40, 0.0003, 0.0003),
        nodata=None,
    )
    cfg = ExtractionConfig(coordinate_crs="EPSG:4326", mode="metric_circle")
    with rasterio.open(path) as ds:
        result = extract_point(ds, 116.00075, 39.99925, 27, cfg)
    # At 40 degrees latitude, E/W cells are about 25.6 m away; N/S about 33.3 m.
    assert result.eligible_count == 3
    assert result.mean == pytest.approx(12)


def test_outside_center_and_empty_valid_window(raster_factory):
    path = raster_factory([[0, 0], [0, 0]])
    with rasterio.open(path) as ds:
        outside = extract_point(ds, 115, 40, 30, config())
        empty = extract_point(ds, *ds.xy(0, 0), 30, config())
    assert outside.status == "outside_extent"
    assert outside.eligible_count == 0
    assert outside.mean is None
    assert empty.status == "no_valid_cells"
    assert empty.mean is None


def test_pixel_limit_prevents_unbounded_read(raster_factory):
    path = raster_factory(np.ones((5, 5)))
    with rasterio.open(path) as ds, pytest.raises(ValueError, match="pixel limit"):
        extract_point(ds, *ds.xy(2, 2), 300, config(max_window_pixels=10))


def test_legacy_rejects_projected_and_south_up_grids(raster_factory):
    cfg = ExtractionConfig(coordinate_crs="EPSG:32650")
    path = raster_factory(
        np.ones((3, 3)),
        crs="EPSG:32650",
        transform=from_origin(500000, 3400000, 30, 30),
    )
    with rasterio.open(path) as ds, pytest.raises(ValueError, match="geographic"):
        extract_point(ds, *ds.xy(1, 1), 30, cfg)
    path = raster_factory(
        np.ones((3, 3)),
        name="south_up.tif",
        transform=rasterio.Affine(0.001, 0, 116, 0, 0.001, 40),
    )
    with rasterio.open(path) as ds, pytest.raises(ValueError, match="north-up"):
        extract_point(ds, *ds.xy(1, 1), 30, config())


@pytest.mark.parametrize("radius", [500, 5000, 50000, 100000])
def test_metric_circle_matches_full_raster_geodesic_reference(raster_factory, radius):
    from pyproj import Geod

    path = raster_factory(
        np.ones((301, 301)),
        crs="EPSG:4326",
        transform=from_origin(116, 40, 0.01, 0.01),
        nodata=None,
    )
    cfg = ExtractionConfig(coordinate_crs="EPSG:4326", mode="metric_circle")
    with rasterio.open(path) as ds:
        lon, lat = ds.xy(150, 150)
        result = extract_point(ds, lon, lat, radius, cfg)
        rows, cols = np.indices((ds.height, ds.width))
        lons = ds.transform.c + (cols + 0.5) * ds.transform.a
        lats = ds.transform.f + (rows + 0.5) * ds.transform.e
        _, _, distances = Geod(ellps="WGS84").inv(
            np.full(lons.shape, lon), np.full(lats.shape, lat), lons, lats
        )
    assert result.eligible_count == int(np.count_nonzero(distances <= radius))
    assert result.valid_count == result.eligible_count


@pytest.mark.parametrize(
    "transform,match",
    [
        (from_origin(179.99, 40, 0.001, 0.001), "dateline"),
        (from_origin(116, 89.95, 0.001, 0.001), "polar"),
    ],
)
def test_unsupported_metric_footprints_are_rejected(raster_factory, transform, match):
    path = raster_factory(np.ones((3, 3)), transform=transform)
    cfg = ExtractionConfig(coordinate_crs="EPSG:4326", mode="metric_circle")
    with rasterio.open(path) as ds, pytest.raises(ValueError, match=match):
        extract_point(ds, *ds.xy(1, 1), 5000, cfg)


def test_scale_offset_is_explicit_and_zero_counts_remain_raw(raster_factory):
    path = raster_factory(np.arange(9).reshape(3, 3))
    with rasterio.open(path, "r+") as ds:
        ds.scales = (0.5,)
        ds.offsets = (2.0,)
    cfg = config(mask_policy="include_zero_nodata", apply_scale=True)
    with rasterio.open(path) as ds:
        result = extract_point(ds, *ds.xy(1, 1), 30, cfg)
    assert result.mean == 4
    assert result.minimum == 2
    assert result.maximum == 6
    assert result.zero_count == 1


def test_missing_raster_crs_rejected(raster_factory):
    path = raster_factory(np.ones((3, 3)), crs=None)
    with rasterio.open(path) as ds, pytest.raises(ValueError, match="Raster CRS"):
        extract_point(ds, 116, 40, 30, config())


def test_center_pixel_records_raw_value_and_policy_validity(raster_factory):
    path = raster_factory([[1, 2, 3], [4, 0, 6], [7, 8, 9]])
    with rasterio.open(path) as ds:
        respected = extract_point(ds, *ds.xy(1, 1), 30, config())
        included = extract_point(
            ds, *ds.xy(1, 1), 30, config(mask_policy="include_zero_nodata")
        )
    assert respected.center_pixel_raw == 0
    assert respected.center_pixel_value is None
    assert not respected.center_pixel_valid
    assert included.center_pixel_raw == included.center_pixel_value == 0
    assert included.center_pixel_valid


def test_center_scale_overflow_is_rejected_even_without_eligible_centers(
    raster_factory,
):
    path = raster_factory(
        [[2]],
        crs="EPSG:32650",
        nodata=None,
        transform=from_origin(500000, 3400000, 30, 30),
    )
    with rasterio.open(path, "r+") as ds:
        ds.scales = (1e308,)
    cfg = ExtractionConfig(
        coordinate_crs="EPSG:32650", mode="metric_circle", apply_scale=True
    )
    with rasterio.open(path) as ds, pytest.raises(ValueError, match="nonfinite"):
        extract_point(ds, 500001, 3399999, 1, cfg)
