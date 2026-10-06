import csv
import json
from pathlib import Path

import numpy as np
import pytest
from rasterio.transform import from_origin

from agb_linkage.cli import main
from agb_linkage.config import ExtractionConfig, load_config
from agb_linkage.inputs import read_locations
from agb_linkage.pipeline import run_extraction


def write_points(path: Path, body: str) -> Path:
    path.write_text("location_id,year,x,y\n" + body, encoding="utf-8")
    return path


@pytest.mark.parametrize("crs", ["GCJ02", "GCJ-02", "BD-09", "unresolved", ""])
def test_unresolved_coordinate_system_rejected(crs):
    with pytest.raises(ValueError, match="coordinate CRS"):
        ExtractionConfig(coordinate_crs=crs)


@pytest.mark.parametrize(
    "body,match",
    [
        ("a,2020,500015,3399985\na,2020,500030,3399970\n", "Duplicate"),
        ("a,2020.5,500015,3399985\n", "integer year"),
        ("a,1899,500015,3399985\n", "year range"),
        ("a,2020,nan,3399985\n", "finite"),
        (",2020,500015,3399985\n", "location ID"),
    ],
)
def test_input_validation(tmp_path, body, match):
    path = write_points(tmp_path / "points.csv", body)
    with pytest.raises(ValueError, match=match):
        read_locations(path, ExtractionConfig(coordinate_crs="EPSG:32650"))


def test_geographic_coordinates_range_checked(tmp_path):
    path = write_points(tmp_path / "points.csv", "a,2020,190,40\n")
    with pytest.raises(ValueError, match="longitude"):
        read_locations(path, ExtractionConfig(coordinate_crs="EPSG:4326"))


def test_input_column_mapping_preserves_leading_zero_ids(tmp_path):
    path = tmp_path / "points.csv"
    path.write_text("stkcd,year,lon,lat\n000001,2020,116,40\n", encoding="utf-8")
    cfg = ExtractionConfig(
        coordinate_crs="EPSG:4326", id_column="stkcd", x_column="lon", y_column="lat"
    )
    assert read_locations(path, cfg)[0].location_id == "000001"


def test_missing_year_is_not_silently_skipped(tmp_path):
    path = write_points(tmp_path / "points.csv", "a,2020,500015,3399985\n")
    cfg = ExtractionConfig(coordinate_crs="EPSG:32650")
    with pytest.raises(FileNotFoundError, match="2020"):
        run_extraction(path, tmp_path, tmp_path / "out.csv", cfg)
    assert not (tmp_path / "out.csv").exists()


def test_pipeline_manifest_and_missing_year_record(raster_factory, tmp_path):
    raster_factory(
        np.ones((3, 3)),
        crs="EPSG:32650",
        transform=from_origin(500000, 3400000, 30, 30),
    )
    path = write_points(
        tmp_path / "points.csv", "000001,2020,500045,3399955\na,2021,500045,3399955\n"
    )
    cfg = ExtractionConfig(
        coordinate_crs="EPSG:32650",
        mode="metric_circle",
        radii_m=(50,),
        missing_year_policy="record",
    )
    output = tmp_path / "out.csv"
    manifest_path = run_extraction(path, tmp_path, output, cfg)
    with output.open() as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["location_id"] == "000001"
    assert rows[0]["valid_count"] == "9"
    assert rows[1]["status"] == "missing_raster"
    manifest = json.loads(manifest_path.read_text())
    assert manifest["input_sha256"]
    assert manifest["config"]["coordinate_crs"] == "EPSG:32650"
    assert manifest["config"]["mask_policy"] == "respect"
    assert manifest["rasters"]["2020"]["crs_authority"] == ["EPSG", "32650"]
    assert manifest["rasters"]["2020"]["nodata"] == 0
    assert manifest["status_counts"] == {"ok": 1, "missing_raster": 1}
    assert manifest["output_sha256"]


def test_no_overwrite_or_input_collision(raster_factory, tmp_path):
    raster_factory(
        np.ones((3, 3)),
        crs="EPSG:32650",
        transform=from_origin(500000, 3400000, 30, 30),
    )
    path = write_points(tmp_path / "points.csv", "a,2020,500045,3399955\n")
    cfg = ExtractionConfig(
        coordinate_crs="EPSG:32650", mode="metric_circle", radii_m=(50,)
    )
    output = tmp_path / "out.csv"
    run_extraction(path, tmp_path, output, cfg)
    with pytest.raises(FileExistsError):
        run_extraction(path, tmp_path, output, cfg)
    with pytest.raises(ValueError, match="input"):
        run_extraction(path, tmp_path, path, cfg)


def test_config_loading_is_immutable_and_rejects_unknown_fields(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("coordinate_crs: EPSG:4326\nradii_m: [500, 1000]\n")
    cfg = load_config(path)
    assert cfg.radii_m == (500, 1000)
    with pytest.raises((AttributeError, TypeError)):
        cfg.mode = "metric_circle"
    path.write_text("coordinate_crs: EPSG:4326\nunknown_field: true\n")
    with pytest.raises(ValueError, match="Unknown"):
        load_config(path)


def test_cli_inspection_and_extract(raster_factory, tmp_path, capsys):
    raster = raster_factory(
        np.ones((3, 3)),
        crs="EPSG:32650",
        transform=from_origin(500000, 3400000, 30, 30),
    )
    assert main(["inspect-raster", str(raster)]) == 0
    metadata = json.loads(capsys.readouterr().out)
    assert metadata["width"] == 3
    points = write_points(tmp_path / "points.csv", "a,2020,500045,3399955\n")
    output = tmp_path / "out.csv"
    assert (
        main(
            [
                "extract",
                "--points",
                str(points),
                "--rasters",
                str(tmp_path),
                "--out",
                str(output),
                "--coordinate-crs",
                "EPSG:32650",
                "--mode",
                "metric_circle",
                "--radii-m",
                "31",
            ]
        )
        == 0
    )
    assert output.exists()
    assert json.loads(capsys.readouterr().out)["manifest"]


def test_cli_config_validation_error(tmp_path, capsys):
    assert (
        main(
            [
                "extract",
                "--points",
                str(tmp_path / "points.csv"),
                "--rasters",
                str(tmp_path),
                "--out",
                str(tmp_path / "out.csv"),
                "--coordinate-crs",
                "GCJ02",
                "--mode",
                "metric_circle",
            ]
        )
        == 2
    )
    assert "coordinate CRS" in capsys.readouterr().err


@pytest.mark.parametrize("field", ["band", "max_window_pixels"])
@pytest.mark.parametrize("value", [1.5, True, False, "1", 0, -1])
def test_integer_settings_are_strict(field, value):
    with pytest.raises(ValueError, match="positive integer"):
        ExtractionConfig(coordinate_crs="EPSG:4326", **{field: value})


def test_second_record_failure_removes_temporary_output(
    raster_factory, tmp_path, monkeypatch
):
    import agb_linkage.pipeline as pipeline

    raster_factory(
        np.ones((3, 3)),
        crs="EPSG:32650",
        transform=from_origin(500000, 3400000, 30, 30),
    )
    points = write_points(
        tmp_path / "points.csv", "a,2020,500045,3399955\nb,2020,500045,3399955\n"
    )
    output = tmp_path / "out.csv"
    cfg = ExtractionConfig(
        coordinate_crs="EPSG:32650", mode="metric_circle", radii_m=(50,)
    )
    original = pipeline.extract_point
    calls = 0

    def fail_second(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise ValueError("deliberate second-record failure")
        return original(*args, **kwargs)

    monkeypatch.setattr(pipeline, "extract_point", fail_second)
    with pytest.raises(ValueError, match="second-record"):
        run_extraction(points, tmp_path, output, cfg)
    assert not output.exists()
    assert not output.with_suffix(".csv.manifest.json").exists()
    assert not list(tmp_path.glob("*.tmp"))
    assert not list(tmp_path.glob(".*.tmp"))


def test_raster_hash_metadata(raster_factory):
    from agb_linkage.metadata import inspect_raster

    path = raster_factory(np.ones((3, 3)))
    metadata = inspect_raster(path, hash_file=True)
    assert len(metadata["sha256"]) == 64
    assert metadata["mask_flags"] == [["nodata"]]


def test_non_degree_geographic_crs_rejected():
    with pytest.raises(ValueError, match="degree"):
        ExtractionConfig(coordinate_crs="EPSG:4807")
