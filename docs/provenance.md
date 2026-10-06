# Provenance and current evidence

Status on 6 October 2026: a recovered company-year table and original producer are available for audit. The actual raster drive is unavailable. Public CFATD metadata have been researched as a candidate source; input lineage is not yet confirmed.

## Recovered lineage

The historical office-address workbook contains 63,441 rows for 5,633 firms over 2000–2023. The geocoded CSV contains 63,312 successful-response firm-years for 5,631 firms. The research-panel extraction `AGB_rebuilt_2026-08-28.csv` contains the 49,022 geocoded firm-years in 2007–2022, representing 5,302 firms. It has one row per stock-code/year key. Source-population coverage and the narrower research-panel period must be reported separately.

The August producer has been recovered from historical records. It reads year-specific `AGB_YEAR.tif` files, retains unmasked numeric cells, emits a point value and three square-window means, and serialises means to four decimal places. It does not transform coordinates or apply a scale/offset. A separate later implementation and archived 200-row comparison provide replication evidence, not a substitute for fresh source validation.

The reconstructed table retains coordinates exactly equal to those in the original geocoded table for all 49,022 joined observations. That equality does not demonstrate spatial correctness or a CRS conversion. The original geocoding scripts parse Amap coordinates directly; source documentation identifies Amap's system as GCJ-02. [Amap coordinate documentation](https://lbs.amap.com/api/javascript-api-v2/guide/abc/basetype)

Preserve the original file as a historical artifact. Any corrected coordinate or mask specification will produce a separately named and versioned result, with a report explaining changes.

## Candidate ecological source

The candidate is the China Annual Forest Aboveground Biomass Time-Series Dataset (CFATD). Its published source article is Cai et al. (2025), *Dynamics of China's forest carbon storage: the first 30 m annual aboveground biomass mapping from 1985 to 2023*, Earth System Science Data, 17, 6993–7018, DOI [10.5194/essd-17-6993-2025](https://essd.copernicus.org/articles/17/6993/2025/). The article links six data records and describes a forest-specific product; it cautions about local-scale use. These product facts do not verify that CFATD was the actual matching input.

| Candidate archive | Coverage | Version-record DOI | Public metadata publication date |
|---|---|---|---|
| Part I | 1985–1993 | [10.5281/zenodo.12620984](https://zenodo.org/records/12620984) | 2 July 2024 |
| Part II | 1994–2001 | [10.5281/zenodo.12637101](https://zenodo.org/records/12637101) | 3 July 2024 |
| Part III | 2002–2008 | [10.5281/zenodo.12655492](https://zenodo.org/records/12655492) | 4 July 2024 |
| Part IV | 2009–2015 | [10.5281/zenodo.12658255](https://zenodo.org/records/12658255) | 4 July 2024 |
| Part V | 2016–2021 | [10.5281/zenodo.12742210](https://zenodo.org/records/12742210) | 15 July 2024 |
| Part VI | 2022–2023 | [10.5281/zenodo.12747329](https://zenodo.org/records/12747329) | 16 July 2024 |

The metadata dates above differ from the 2025 dates in the source paper's reference list. Record-level citations should use the actual archive metadata consistently. The source paper's final DOI replaces its earlier discussion-preprint DOI; the Zenodo description still contains that older preprint citation. Dataset authorship also differs from the final paper author list: preserve the appropriate creator list for each research object.

The public record descriptions identify values as biomass density in Mg/ha, say uncertainty layers are available through GEE rather than the offline archive, and flag occasional unusually high values. For this project's recovered table, units remain provisional until actual input identity and encoding are confirmed. Do not convert density into total biomass by merely relabelling the field. [Candidate Part I metadata](https://zenodo.org/records/12620984)

## Direct public-header check

`upstream_geotiff_probe.json` records bounded HTTP range inspection of only TIFF metadata for public candidate `AGB_2007.tif`, Part III. The successful probe read 867 bytes and no raster cells. Observed metadata are EPSG:4326/WGS84, unsigned 16-bit storage, NoData=0, grid width 228,538 and height 132,983, and a cell step of 0.00026949458523585647 degrees on both axes. The GDAL metadata contains no scale or offset entries; their absence is not a confirmation of units or zero semantics.

Historical metadata recovered for the user's 2015 raster have the same CRS, grid dimensions, data type, NoData value and angular cell step. This strengthens the candidate match but does not prove file identity. Confirm annual hashes or the actual GEE export lineage when inputs are restored. The source article says its linked GEE script requires login; its executable source was not inspected in this session. [Provider file](https://zenodo.org/api/records/12655492/files/AGB_2007.tif/content), [Source data availability](https://essd.copernicus.org/articles/17/6993/2025/)

## Unresolved interpretation

NoData=0 is a file encoding, not independent evidence that every zero represents ecological absence. The recovered producer's assertion that zero is genuine inside China is a historical rationale requiring provider-supported validation. Determine forest versus nonforest semantics, geographic background, water, missing coverage and any source masks before assigning a scientific denominator.

The candidate paper defines annual forest extent using tree cover of at least 20%. It calculates total forest biomass from biomass density multiplied by forest area, where forest area incorporates forest-cover fraction and pixel area. Neither the main article nor its supplement explicitly resolves the zero/background encoding needed here. Anonymous access to the linked GEE script redirects to Google sign-in, so its mask/export implementation was not inspected. [Source methods, sections 2.1.2 and 2.7](https://essd.copernicus.org/articles/17/6993/2025/), [Supplement](https://essd.copernicus.org/articles/17/6993/2025/essd-17-6993-2025-supplement.pdf), [Provider GEE link](https://code.earthengine.google.com/4f8ad8d32ddb84e826e941a95f31f9be)

Even establishing valid nonforest zeros would not, by itself, justify calling the unweighted mean a landscape biomass density. Under the candidate paper's biomass accounting, an area-consistent forest-biomass-per-land-area statistic would also need the applicable forest-cover fractions, pixel areas and support denominator. A forest-conditional density mean, a zero-inclusive arithmetic index and total forest biomass are distinct quantities. The final specification must state which it reports.

The original producer computes half-width `round(radius_m / 111000 / cell_step_degrees)` and averages the resulting square. It does not construct a metric circle. Angular east-west lengths vary with latitude, and a valid local-area average may require appropriate area weights. Reproducing these choices preserves provenance; independently assessing them is a separate task.

Before release, attach an exact input manifest, actual source version/DOIs, native raster metadata, coordinate transformation lineage, mask/scale decisions and final output checksums. Required source and field rights are recorded separately in `data_rights.md`.
