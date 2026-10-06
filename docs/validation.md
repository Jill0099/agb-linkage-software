# Validation status

The real panel remains private by the author's publication choice. The shared scope is methods, software and aggregate findings. Evidence separates stored-table integrity, historical comparisons, fresh numerical reproduction, software tests and unresolved geographic/ecological interpretation.

## Evidence completed on 6 October 2026

| Check | Result | What it establishes |
|---|---|---|
| Recovered panel population | 49,022 rows; 5,302 stock codes; 2007–2022; no duplicate firm-year keys | Stored file population and unique keys |
| File identity | Local and Mac mini copies share SHA-256 `e00cc7c1eff631d2963746a1df6def68432f2bff0b8525855c5db8bc21fb18f8` | Same saved bytes on both machines |
| Source-coordinate join | All 49,022 panel keys match the original geocoding table | Address-table lineage |
| Coordinate comparison | Longitude and latitude differences equal zero for every matched row | No observed later coordinate correction; not evidence of correct CRS |
| Legacy point comparison | 5,681 overlapping nonmissing point values all agree within 0.001 | Agreement where both files contain a value |
| Legacy missingness | 43,341 rebuilt zero-valued points were missing in the legacy file | Difference in stored missingness; zero's ecological meaning still unresolved |
| Archived 200-row comparison | All 200 saved comparison outputs agree at nominal 500 m and 1 km within 0.001; maximum mean discrepancies approximately 0.00005; all denominator counts identical | Rechecking archived output against the frozen panel, distinct from the fresh extraction reported below |
| Original producer recovery | Exact historical August extraction script recovered, with historical native raster metadata | Recovered algorithm and source identity; all 16 annual full-file comparisons are complete on restored inputs |
| Restored source access | 39 annual rasters accessible; actual native metadata checked, including all 16 panel years in the fresh sample run | Actual input encoding and fingerprint consistency; not complete file identity |
| Native encoding | EPSG:4326, uint16, one band, NoData=0, scale 1, offset 0 and NoData-derived mask | File storage/reference metadata; numeric zero is not thereby validated as ecological absence |
| Provider sizes | All 16 panel-year file sizes match official CFATD metadata | Supporting source-identity evidence |
| Complete provider checksum | All 16 files for 2007–2022 match official CFATD Parts III–VI sizes and MD5s; each file unchanged during its read | Exact provider-file identity for all 16 research-panel years, totalling 111,427,926,212 bytes; not a check of all 39 files |
| Fresh preserved-sample extraction | 200/200 point values exact; 600/600 square means exact after four-decimal serialization; 600/600 cell counts exact | Fresh numerical reproduction under the historical zero-inclusive coordinate-passthrough specification |

## Fresh numerical check and its scope

The new read-only run reuses the preserved historical 200-point-year list, covering 2007–2022 with 4–23 cases per year. No new random draw or stratification occurred; the selection seed and representativeness are not established. It samples actual restored annual rasters, retains every numeric zero, and applies no coordinate correction or reprojection. A declared mean tolerance of 0.001 was met in every case, with observed maximum difference zero after the original four-decimal serialization. The three square specifications are checked separately, including the widest support.

This result reproduces a computation. It does not independently establish office placement, a scientifically appropriate mask denominator or metric-circle geometry. It should not be described as 200 geographically validated company locations.

## Measurement sensitivity observed in the saved table

Pooled over all 49,022 firm-years, using average ranks for ties, Spearman correlations are 0.9073 between the 35-by-35 and 67-by-67 square means, and 0.7601 between the 67-by-67 and 335-by-335 means. Relative to the 67-by-67 mean, absolute rank shifts above 10 percentile points occur in 16,203 rows (33.05%) for the smaller square and 25,899 rows (52.83%) for the larger square.

These are deterministic descriptive comparisons of the historical pixel-square definitions. They are not evidence for circular-radius robustness, causal effects, geocoding accuracy, or correctly measured biomass. Provider metadata identifies source forest biomass density in Mg/ha; the historical zero-inclusive denominator and meaning of numeric zero require separate interpretation. Computing ranks separately within each year gives affected shares of 34.94%–42.56% for the smaller square and 53.08%–56.11% for the larger square across 2007–2022. Thus the sensitivity is also present in within-year rankings, without establishing that any specification is ecologically correct.

## Zero values and denominator semantics

Stored zero counts are 43,341 for point sampling, 1,418 for the 35-by-35 mean, 278 for the 67-by-67 mean, and 15 for the 335-by-335 mean. Every panel row has counts 1,225, 4,489, and 112,225 respectively. Those counts represent the stored averaging denominator, not an independently validated count of ecological observations.

The historical producer reads unmasked pixels and retains zero. Reproduction of this convention is explicitly labelled legacy replication. Retaining a NoData value does not automatically convert it to an observed ecological zero. Missing coverage, raster background, nonforest and true zero require product-specific interpretation.

## Coordinate precision

The successful Amap responses include varying match levels. In the rebuilt panel, counts include 956 unknown-level, 667 district/county-level, 172 city-level, 1,292 township-level and 1,120 village-level records. Finer match labels are not independent accuracy measurements. The actual original geocoding/resume scripts directly split Amap's response location string, with no reference-system conversion in the recovered chain. All panel coordinates persist unchanged; their documented GCJ-02 lineage remains unreconciled with the actual EPSG:4326 raster before a geographically revised measure can be endorsed.

## Remaining checks and separately scoped extensions

- Retain the completed [all-year source verification](source_file_verification.json), exact Parts III–VI citations, native metadata and preserved-sample numerical check as completed evidence.
- Maintain the distinction between provider-documented density units, actual scale/offset and scientifically unresolved zero/mask denominators.
- Independent address/coordinate placement assessment and permitted coordinate transformation/acquisition.
- The historical point and three nominal-square specifications are freshly reproduced on the preserved sample; corrected metric-circle/coordinate comparisons are future scientific extensions.
- Selection/sensitivity by coordinate precision and comparison to independently verified location placement.
- Real tables, addresses, identifiers and coordinates remain private. A public full-panel dataset or project dataset DOI is not a remaining deliverable; any future data release needs a separate author decision and applicable rights evidence.

## Reproducibility

`scripts/audit_tables.py` reads user-supplied paths and writes an aggregate JSON plus standalone figures. It exports no record-level table. Input paths and hashes in the JSON should stay in a private audit directory. The software's synthetic example and automated tests are separate from these real-data checks and cannot certify the recovered real dataset.
