# Chinese listed-company locations × aboveground biomass

**Yueyang Wang · Cardiff University**

This project documents and reproduces a workflow linking company location-years
to third-party aboveground biomass (AGB) rasters. The original contribution is
the corporate-location linkage, extraction definitions, auditing and reproducible
software. The upstream satellite-derived AGB estimates belong to their creators
and require separate attribution.

## Current status

Software version **0.1.0**, including code, documentation and synthetic examples,
is publicly archived at [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348).
This software DOI identifies the archived software, not the real matched dataset.
The public [software repository](https://github.com/Jill0099/agb-linkage-software)
provides the maintained code and citation instructions. The manuscript review
repository remains private. All 66 local tests pass, with 91% core software coverage. A recovered real-data candidate
contains 49,022 firm-years for 5,302 Chinese
listed companies during 2007–2022. It is **not a publicly released dataset**:
the user has selected a methods-and-aggregate-results publication with company-level
records kept private. Fresh reproduction of 200 historical location-years now matches
all point values and all three square means/counts at the saved precision. All sixteen annual source files match official CFATD file sizes and MD5 checksums.
Coordinate reference and ecological zero interpretation remain limits on scientific
use of the historical measures.

The locations originate from office-address records. They have not been
established as operating facilities. The saved AGB fields describe historical
pixel squares, whose nominal metre labels must not be interpreted as verified
circular buffers. AGB is a biomass measure; this project does not establish
corporate biodiversity impact or causal financial effects.

See [methodology](docs/methodology.md), [provenance](docs/provenance.md),
[validation](docs/validation.md), [source rights](docs/data_rights.md), and the
[candidate field dictionary](docs/data_dictionary.csv). Public companion reports
include [aggregate table results](docs/stored_table_aggregate_summary.json),
[fresh numerical replication](docs/fresh_replication_summary.json),
[native raster metadata](docs/native_source_metadata.json),
[complete annual source-file verification](docs/source_file_verification.json), and
[hypothetical latitude-dependent window dimensions](docs/angular_window_geometry.csv).

## Install and run a synthetic example

Python 3.12 and [uv](https://docs.astral.sh/uv/) are required for the locked
development environment.

```bash
uv sync --frozen --no-editable
uv run --frozen --no-editable python examples/demo.py --out-dir outputs/synthetic-demo
uv run --frozen --no-editable agb-linkage inspect-raster outputs/synthetic-demo/AGB_2020.tif
uv run --frozen --no-editable pytest --cov=agb_linkage --cov-report=term-missing
```

The example creates a tiny artificial raster and invented location identifiers.
It uses no company data, provider credentials, or source-drive files. Select a
new output directory if the demonstration has already run.

## Extract from your own authorised inputs

Prepare a CSV with the configured identifier, year, x and y fields and annual
GeoTIFFs named `AGB_{year}.tif`. Identify the coordinate CRS from its actual
provenance. Assigning an EPSG label does not convert GCJ-02 coordinates to WGS84.

```bash
uv run --frozen --no-editable agb-linkage extract \
  --points /path/to/authorised_locations.csv \
  --rasters /path/to/annual_rasters \
  --out outputs/my_extraction.csv \
  --config configs/metric_circle.yaml \
  --coordinate-crs EPSG:4326
```

Replace the CRS only with the verified CRS of your input, rather than copying the
example declaration. Template configurations deliberately use `unresolved` and
will fail until an explicit supported CRS is supplied. GCJ-02 and unknown CRS
labels are rejected. The pipeline does not provide a geocoding service or assert
permission to obtain, transform or redistribute provider outputs.

The two extraction strategies are:

- `legacy_pixel_square`: reproduce the recovered historical angular-grid window
  rule on supported geographic grids, with explicit mask/zero settings.
  Reproduction is conditional on compatible source metadata and values.
- `metric_circle`: select pixel centres by WGS84 geodesic distance, with coordinate
  transformations and explicit data-validity policies. This is a different
  measurement specification and should receive a separate version if used to
  replace historical statistics.

Extraction writes a long-format output and a run manifest describing configuration,
input identity, native raster metadata and processing status. Eligible, valid and
zero counts should be interpreted using the selected policy. Do not place real
input/output data in a public repository without permission.

## Reproduce the stored-table audit

Install the optional analysis dependencies:

```bash
uv sync --frozen --no-editable --extra analysis
uv run --frozen --no-editable --extra analysis python scripts/audit_tables.py \
  --coordinates /path/to/coordinate_table.csv \
  --rebuilt /path/to/rebuilt_candidate.csv \
  --legacy /path/to/legacy_long_table.csv \
  --output-dir private/audit
uv run --frozen --no-editable --extra analysis pytest scripts/tests/test_audit_tables.py
```

An optional `--addresses /path/to/office_addresses.xlsx` includes the original
address population in the audit. The script produces aggregate JSON and figures,
not record-level exports. Its manifest includes private input paths; keep that
output private. The reported stored-data sensitivity does not replace fresh
raster, coordinate or ecological validation.

## Paper, archive and citation

The English measurement working paper was submitted to SSRN on 6 October 2026:
[SSRN Abstract ID 7570918](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7570918).
SSRN has confirmed receipt; screening remains pending. Its abstract page is
accessible in the verified browser session. The paper uses CC BY 4.0 and is
excluded from the fixed software archive. It reports stored-table findings,
fresh historical numerical reproduction and the remaining coordinate and
ecological interpretation limits. No paper DOI, dataset DOI or public real-data
archive is claimed.

See [CITATION.md](CITATION.md) for the software citation and the distinct paper,
derived-data and upstream citations. `CITATION.cff` supplies structured software
metadata and a working-paper preferred citation. The current release publishes methods and aggregate evidence; the real panel
remains private. A future data citation will be added only if a separately cleared
data record is actually published.

## Licence

New project software and its documentation are available under [MIT](LICENSE).
This does not license third-party rasters, company/address inputs, geocoding
outputs or the real-data candidate. Synthetic demonstration inputs are covered
by the software licence. Source-specific rights and exclusions are documented
separately.
