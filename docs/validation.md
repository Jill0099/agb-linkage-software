# Validation status

The rebuilt real-data candidate is **not a validated public dataset**. Current evidence separates stored-table checks, comparisons with previously saved outputs, new software tests, and the outstanding fresh raster/geocoding audit.

## Evidence completed on 6 October 2026

| Check | Result | What it establishes |
|---|---|---|
| Candidate population | 49,022 rows; 5,302 stock codes; 2007–2022; no duplicate firm-year keys | Stored file population and unique keys |
| File identity | Local and Mac mini copies share SHA-256 `e00cc7c1eff631d2963746a1df6def68432f2bff0b8525855c5db8bc21fb18f8` | Same saved bytes on both machines |
| Source-coordinate join | All 49,022 candidate keys match the original geocoding table | Address-table lineage |
| Coordinate comparison | Longitude and latitude differences equal zero for every matched row | No observed later coordinate correction; not evidence of correct CRS |
| Legacy point comparison | 5,681 overlapping nonmissing point values all agree within 0.001 | Agreement where both files contain a value |
| Legacy missingness | 43,341 rebuilt zero-valued points were missing in the legacy file | Difference in stored missingness; zero's ecological meaning still unresolved |
| Archived 200-row comparison | All 200 saved comparison outputs agree at nominal 500 m and 1 km within 0.001; maximum mean discrepancies approximately 0.00005; all denominator counts identical | Rechecking archived output against the frozen candidate, not rerunning extraction today |
| Original producer recovery | Exact historical August extraction script recovered, with historical native raster metadata | Stronger algorithm provenance; source checksums still require original input access |

## Measurement sensitivity observed in the saved table

Pooled over all 49,022 firm-years, using average ranks for ties, Spearman correlations are 0.9073 between the 35-by-35 and 67-by-67 square means, and 0.7601 between the 67-by-67 and 335-by-335 means. Relative to the 67-by-67 mean, absolute rank shifts above 10 percentile points occur in 16,203 rows (33.05%) for the smaller square and 25,899 rows (52.83%) for the larger square.

These are deterministic descriptive comparisons of the historical pixel-square definitions. They are not evidence for circular-radius robustness, causal effects, geocoding accuracy, or correctly measured biomass. Physical units and the meaning of numeric zero must be established separately. Computing ranks separately within each year gives affected shares of 34.94%–42.56% for the smaller square and 53.08%–56.11% for the larger square across 2007–2022. Thus the sensitivity is also present in within-year rankings, without establishing that any specification is ecologically correct.

## Zero values and denominator semantics

Stored zero counts are 43,341 for point sampling, 1,418 for the 35-by-35 mean, 278 for the 67-by-67 mean, and 15 for the 335-by-335 mean. Every candidate row has counts 1,225, 4,489, and 112,225 respectively. Those counts represent the stored averaging denominator, not an independently validated count of ecological observations.

The historical producer reads unmasked pixels and retains zero. Reproduction of this convention is explicitly labelled legacy replication. Retaining a NoData value does not automatically convert it to an observed ecological zero. Missing coverage, raster background, nonforest and true zero require product-specific interpretation.

## Coordinate precision

The successful Amap responses include varying match levels. In the rebuilt candidate, counts include 956 unknown-level, 667 district/county-level, 172 city-level, 1,292 township-level and 1,120 village-level records. Finer match labels are not independent accuracy measurements. Original Amap coordinates persist unchanged in the candidate; their GCJ-02 lineage must be reconciled with the historically EPSG:4326 raster before scientifically revised measures are endorsed.

## Remaining checks

- Fresh extraction from the user's actual raster files, with current hashes and native metadata.
- Source identity/version agreement with upstream DOI records, units, scale and zero/mask conventions.
- Independent address/coordinate placement assessment and permitted coordinate transformation/acquisition.
- Point, 500 m, 1 km and 5 km reproduction plus correctly defined metric-circle comparisons.
- Selection/sensitivity by coordinate precision and comparison to independently verified location placement.
- Explicit rights clearance for any real table, address, identifier or coordinate distributed publicly.

## Reproducibility

`scripts/audit_tables.py` reads user-supplied paths and writes an aggregate JSON plus standalone figures. It exports no record-level table. Input paths and hashes in the JSON should stay in a private audit directory. The software's synthetic example and automated tests are separate from these real-data checks and cannot certify the recovered real dataset.
