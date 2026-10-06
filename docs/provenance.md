# Provenance and current evidence

Status on 6 October 2026: the source drive is restored, with 39 annual rasters accessible. The recovered panel, original producer, actual native metadata and fresh preserved-sample numerical reproduction are available for audit. Complete file-size and MD5 comparisons match all 16 research-panel inputs from 2007–2022 to official CFATD Parts III–VI, with each file unchanged during its read. The author has chosen to share methods and aggregate results while keeping real observations private.

## Recovered lineage

The historical office-address workbook contains 63,441 rows for 5,633 firms over 2000–2023. The geocoded CSV contains 63,312 successful-response firm-years for 5,631 firms. The research-panel extraction `AGB_rebuilt_2026-08-28.csv` contains the 49,022 geocoded firm-years in 2007–2022, representing 5,302 firms. It has one row per stock-code/year key. Source-population coverage and the narrower research-panel period must be reported separately.

The August producer has been recovered from historical records. It reads year-specific `AGB_YEAR.tif` files, retains unmasked numeric cells, emits a point value and three square-window means, and serialises means to four decimal places. It does not transform coordinates or apply a scale/offset. An archived 200-row comparison is historical evidence. A new read-only extraction from the restored rasters now reproduces the preserved 200 cases across all three square specifications; this is fresh numerical evidence, with coordinate and ecological interpretation assessed separately.

The reconstructed table retains coordinates exactly equal to those in the original geocoded table for all 49,022 joined observations. Examination of the actual original geocoding and resume scripts confirms direct splitting of Amap's returned location string. No GCJ-02/WGS84 conversion is present in those scripts or the recovered extraction chain. Source documentation identifies Amap's system as GCJ-02, while actual rasters declare EPSG:4326; that lineage remains unreconciled. Coordinate equality and numerical reproduction do not establish geographic placement. [Amap coordinate documentation](https://lbs.amap.com/api/javascript-api-v2/guide/abc/basetype)

Preserve the original file as a historical artifact. Any corrected coordinate or mask specification will produce a separately named and versioned result, with a report explaining changes.

## Confirmed ecological source

CFATD is the identified provider for every restored 2007–2022 research-panel raster. All 16 complete MD5s and file sizes match official Parts III–VI, covering 111,427,926,212 bytes. Size and modification time were unchanged during each read. This identity check covers the 16 panel-year files, not all 39 rasters in the restored collection. The [year-specific verification summary](source_file_verification.json) gives the expected and observed checksums and original record for each input. Its published source article is Cai et al. (2025), *Dynamics of China's forest carbon storage: the first 30 m annual aboveground biomass mapping from 1985 to 2023*, Earth System Science Data, 17, 6993–7018, DOI [10.5194/essd-17-6993-2025](https://essd.copernicus.org/articles/17/6993/2025/). The article links six data records and describes a forest-specific product; it cautions about local-scale use. Year-specific input identity must be stated rather than inferred from one matching year.

| Confirmed input archive | Archive coverage | Panel years used | Version-record DOI | Public metadata publication date |
|---|---|---|---|---|
| Part III | 2002–2008 | 2007–2008 | [10.5281/zenodo.12655492](https://zenodo.org/records/12655492) | 4 July 2024 |
| Part IV | 2009–2015 | 2009–2015 | [10.5281/zenodo.12658255](https://zenodo.org/records/12658255) | 4 July 2024 |
| Part V | 2016–2021 | 2016–2021 | [10.5281/zenodo.12742210](https://zenodo.org/records/12742210) | 15 July 2024 |
| Part VI | 2022–2023 | 2022 | [10.5281/zenodo.12747329](https://zenodo.org/records/12747329) | 16 July 2024 |

The metadata dates above differ from the 2025 dates in the source paper's reference list. Record-level citations should use the actual archive metadata consistently. The source paper's final DOI replaces its earlier discussion-preprint DOI; the Zenodo description still contains that older preprint citation. Dataset authorship also differs from the final paper author list: preserve the appropriate creator list for each research object.

The public record descriptions identify values as forest biomass density in Mg/ha, say uncertainty layers are available through GEE rather than the offline archive, and flag occasional unusually high values. All 16 panel-year files carry this confirmed provider attribution. These are source density values, while the historical zero-inclusive arithmetic mean retains a scientifically unresolved denominator. The actual native scale is 1 and offset 0. Do not convert density into total biomass by merely relabelling a field. [Part III metadata](https://zenodo.org/records/12655492)

## Direct public-header check

`upstream_geotiff_probe.json` records bounded HTTP range inspection of only TIFF metadata for the public provider file `AGB_2007.tif`, Part III, initially inspected before the restored-file identity was established. The successful probe read 867 bytes and no raster cells. Observed metadata are EPSG:4326/WGS84, unsigned 16-bit storage, NoData=0, grid width 228,538 and height 132,983, and a cell step of 0.00026949458523585647 degrees on both axes. The GDAL metadata contains no scale or offset entries; their absence is not a confirmation of units or zero semantics.

Fresh inspection of the actual 2007, 2015 and 2022 inputs confirms the same CRS, dimensions, data type, NoData value and cell step, together with scale 1, offset 0 and a NoData-derived mask. The fresh sample run checks all 16 research-panel annual fingerprints with no disagreement. Comparing its inventory with official metadata finds exact file-size agreement for all 16 years. Complete MD5 and file-size matches are established for every panel year from 2007 through 2022. The source article says its linked GEE script requires login; its executable source was not inspected in this session. [Provider file](https://zenodo.org/api/records/12655492/files/AGB_2007.tif/content), [Source data availability](https://essd.copernicus.org/articles/17/6993/2025/)

## Fresh preserved-sample reproduction

A read-only extraction on 6 October 2026 reuses the unchanged historical 200-point-year check set, spanning all 16 research-panel years with 4–23 cases per year. All 200 point values match exactly. All 600 square means match after four-decimal serialization, and all 600 cell counts match. This run uses the original numeric coordinates, unmasked zero-inclusive squares and no scaling/reprojection. The check-set selection seed and representativeness are not established; it is a numerical regression check, not a new random spatial-validation sample.

## Unresolved interpretation

NoData=0 is a file encoding, not independent evidence that every zero represents ecological absence. The recovered producer's assertion that zero is genuine inside China is a historical rationale requiring provider-supported validation. Determine forest versus nonforest semantics, geographic background, water, missing coverage and any source masks before assigning a scientific denominator.

The source paper defines annual forest extent using tree cover of at least 20%. It calculates total forest biomass from biomass density multiplied by forest area, where forest area incorporates forest-cover fraction and pixel area. Neither the main article nor its supplement explicitly resolves the zero/background encoding needed here. Anonymous access to the linked GEE script redirects to Google sign-in, so its mask/export implementation was not inspected. [Source methods, sections 2.1.2 and 2.7](https://essd.copernicus.org/articles/17/6993/2025/), [Supplement](https://essd.copernicus.org/articles/17/6993/2025/essd-17-6993-2025-supplement.pdf), [Provider GEE link](https://code.earthengine.google.com/4f8ad8d32ddb84e826e941a95f31f9be)

Even establishing valid nonforest zeros would not, by itself, justify calling the unweighted mean a landscape biomass density. Under the source paper's biomass accounting, an area-consistent forest-biomass-per-land-area statistic would also need the applicable forest-cover fractions, pixel areas and support denominator. A forest-conditional density mean, a zero-inclusive arithmetic index and total forest biomass are distinct quantities. The final specification must state which it reports.

The original producer computes half-width `round(radius_m / 111000 / cell_step_degrees)` and averages the resulting square. It does not construct a metric circle. Angular east-west lengths vary with latitude, and a valid local-area average may require appropriate area weights. Reproducing these choices preserves provenance; independently assessing them is a separate task.

The methods-and-aggregate-results package provides year-specific source identity, native metadata and preserved-sample summaries, together with explicit coordinate/mask limits. The initial public metadata catalogue `upstream_candidates.json` preserves the provider-record snapshot collected before file identity was confirmed; current input identity is reported in `source_file_verification.json`. The real panel and row-level validation keys remain private by author choice. Any independently corrected measure or future real-data release is a separate extension requiring its own scientific and rights evidence. Source-specific evidence is recorded in `data_rights.md`.
