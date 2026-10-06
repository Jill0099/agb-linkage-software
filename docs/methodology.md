# Extraction definitions and measurement choices

The software implements explicit geometry and validity policies. It does not establish a source's units, rights or ecological interpretation. The recovered company-year table is a historical artifact; a new extraction is not a scientifically validated replacement merely because the program completes.

## Observation and inputs

An input row represents one identified location in one year, with x/y coordinates in a verified geographic or projected reference system. Configure the identifier, year and coordinate columns and the annual raster filename template. The supplied configurations leave the coordinate reference `unresolved`; execution requires an explicit supported CRS. GCJ-02 and BD-09 declarations are rejected. A change of label alone is not a coordinate conversion.

The pipeline selects the raster for the row's year and transforms supported input coordinates to its native CRS. A location outside the raster extent receives `outside_extent`, without extracting an overlapping neighbourhood. Missing annual files cause an error by default; an explicit alternative can record `missing_raster` rows. No biomass unit or source identity is inferred from a filename.

## Spatial supports

| Mode | Selected cells | Interpretation |
|---|---|---|
| `legacy_pixel_square` | An inclusive square around the cell containing the point, with half-width `max(1, round(radius_m / 111000 / horizontal_cell_step_degrees))`, clipped at the grid boundary | Reconstructs the recovered angular-grid support rule on compatible geographic grids. The metre field is a historical parameter; it is not a metric circular radius. |
| `metric_circle` | Cell centres within the requested WGS84 ellipsoidal geodesic distance from the location | A separate support definition. Cell-centre inclusion approximates a continuous footprint; it does not assign fractional intersection weights. |

Both modes calculate an arithmetic mean over selected, policy-valid cells. The current software does not provide pixel-area or forest-cover weighting. Thus a metric circle alone does not make its mean a mass-consistent landscape biomass statistic. Choice of source, forest mask and denominator must precede that interpretation. See [provenance](provenance.md).

For the recovered table, the stored squares contain 1,225, 4,489 and 112,225 cells. These are historical window sizes, not counts independently verified as valid ecological pixels.

## Validity, numeric zeros and scaling

`mask_policy: respect` retains the raster's validity mask. `include_zero_nodata` can ignore a mask generated solely from a declared zero NoData value; it preserves independent dataset or alpha masks. That option exposes a historical numerical convention for comparison. It does not establish that all zero-tagged cells are ecological observations.

`zero_policy: include` keeps valid raw zeros. `exclude` removes them from the average after mask/finite-value selection. Neither policy independently identifies forest cells. A positive-cell mean is not automatically a forest-conditional mean: forest cells can have zero predictions, and a positive cell need not satisfy a confirmed forest mask.

Nonfinite values are excluded. By default the program uses stored numeric values without scale/offset. `apply_scale` applies documented raster scale/offset after validity and raw-zero decisions. The provenance record must establish whether that encoding is scientifically appropriate.

## Output and reproducibility record

Output is long format, with one row per input location-year and requested support. It records geometry, status, eligible and valid cell counts, masked/nonfinite/zero counts, summary statistics, clipping and the centre cell. `center_pixel_raw` is the stored native-grid value; `center_pixel_value` reflects the selected policy and optional scaling. Zero counts are calculated on raw values before optional exclusion/scaling.

The run manifest records configuration, software environment, input SHA-256, output SHA-256, raster metadata, year availability and processing statuses. Raster hashing is optional because annual inputs can be large; enable it for a frozen final reproducibility run or otherwise supply independently verified input hashes. Source-name/version/DOI configuration fields are declarations, not automatic verification. Manifests contain input/output paths and should remain private when those paths disclose private information.

Select a new output path for each run: the pipeline refuses to replace an existing output or manifest. Keep the historical output separately when changing coordinates, support, masking, scaling or source version. The [validation record](validation.md) distinguishes completed table checks, historical replication evidence and fresh scientific validation still required.
