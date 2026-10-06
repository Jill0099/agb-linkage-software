# Data rights and release boundaries

Checked 6 October 2026. This document records evidence and release decisions; it does not establish the terms of an institutional contract that has not been inspected.

The project contributes company-location linkage and extraction methods. The source AGB rasters, company-address records, and geocoding responses have separate provenance and rights. A licence on the new software does not license those inputs or all derived tables.

**Author's current publication decision:** keep real observations, addresses and geocoding outputs private; publish methods, software and aggregate audit results. A public full-panel dataset and project dataset DOI are outside the current deliverables. Any later real-data release would require a separate decision and applicable evidence.

## Evidence matrix

| Material | Evidence checked | Current decision | Evidence or separately scoped follow-up |
|---|---|---|---|
| New `agb-linkage` software | New implementation prepared for this project | MIT applies to the project's original software as specified in the root licence; no third-party data rights are granted | Confirm any incorporated third-party code and contributor ownership |
| CFATD source attribution | All 16 restored 2007–2022 research-panel files match official sizes and MD5s in Parts III–VI, whose records list `cc-by-4.0` | Credit the confirmed source creators and exact input records; original rasters are excluded from this project's archive | Retain the verified year-to-record mapping and applicable attribution/licence/change notices |
| Company identifiers and office-address histories | Historical project documentation names CSMAR; export table/version and the applicable institution agreement are unavailable | Keep original exports and linked observations private by author choice | Document provenance and applicable reporting terms; row-level redistribution would be a separate future assessment |
| Amap geocodes and quality fields | Original scripts parse Amap outputs directly; current provider terms and coordinate documentation checked | Saved responses remain private in the chosen scope; no open licence is asserted | Document account/product and collection provenance/reporting terms; any later response or coordinate dissemination would be separately assessed |
| Real company-year AGB linkage | Combines the preceding inputs; audit confirms 49,022 observations in the recovered research panel | Remains private by author choice; no public data licence or dataset DOI assigned | Any future release would assess its exact fields and use against applicable agreements; removing coordinates alone does not establish permission |
| Synthetic demonstration | Artificial raster and fictitious location identifiers generated for demonstrating the software | Can be prepared without distributing real provider responses or listed-company observations | Verify documentation clearly identifies it as synthetic and checksums identify only this demonstration |
| Paper and aggregate audit summaries | Methods, table findings and fresh preserved-sample reproduction exclude row-level firm/address/coordinate records | Chosen publication scope; manuscript remains a local review draft | Confirmed source attribution, accurate scientific limits, author/disclosure approval and any applicable restrictions on the reported information |

## What the provider documents actually say

All six CFATD Zenodo records report the licence identifier `cc-by-4.0` in their public metadata. Complete file-size and MD5 comparisons independently identify the 16 research-panel inputs as files from Parts III–VI. The project's source matching, aggregation and zero-inclusion convention should be described as changes; company/location rights remain separate. [Part I](https://zenodo.org/api/records/12620984), [Part II](https://zenodo.org/api/records/12637101), [Part III](https://zenodo.org/api/records/12655492), [Part IV](https://zenodo.org/api/records/12658255), [Part V](https://zenodo.org/api/records/12742210), [Part VI](https://zenodo.org/api/records/12747329)

CC-BY-4.0 permits sharing and adaptation subject to attribution, a licence link, and indicating changes; it does not remove rights associated with unrelated inputs. For a cleared derivative, identify the AGB authors/product/version, explain the new matching and aggregation, and preserve the source licence information. [Creative Commons licence deed](https://creativecommons.org/licenses/by/4.0/)

Amap's current platform service terms were updated on 3 December 2025. Section 2.2 expressly includes geocoding, coordinates and address data among covered content. Section 4.12 describes restrictions, subject to its stated legal/permission conditions, on copying, derivative works/databases, standalone display and dissemination. These clauses warrant checking the precise account/product agreement and intended derived output. They are not a finding that the user's historical research was unauthorised. Collection logs precede this revision, so the terms applicable to that collection also need verification. [Amap service terms](https://lbs.amap.com/pages/terms/)

A publicly posted CSMAR supplier contract at Tianjin University addresses provision of both database content and processed data to third parties. It is useful evidence that derivative rights can be contract-specific, but it is not the agreement applicable to this project. The provider's public product page describes research and custom-data services without granting a general redistribution licence. [Public supplier-contract example](https://zbb.tju.edu.cn/sfw_cms/r/s/cms/392c81330d28410fb357ba74080b6462/0/CSMAR%E6%95%B0%E6%8D%AE%E5%BA%93%E5%90%88%E5%90%8C.pdf), [CSMAR product information](https://www.csmar.com/channels/31.html)

## Provenance and reporting checks

For CSMAR, identify the original company-information table, export date, subscriber institution and agreement. The current package excludes row-level exports and matching outputs. Any agreement-specific restriction on reporting aggregate information should be addressed using the actual agreement; no blanket permission or prohibition is inferred from another university's contract. A future row-level release would require its own field-specific assessment.

For Amap, identify the account/product and collection period. Saved responses and coordinates remain private in the chosen scope. Document the coordinate lineage and applicable research/reporting terms without claiming an open licence for provider responses. Any later coordinate dissemination or independently sourced reconstruction would need separate provenance and permission evidence.

For the raster product, [source-file verification](source_file_verification.json) records complete size/MD5 matches and exact public record mapping for all 16 research-panel years. The initial `upstream_candidates.json` catalogue preserves provider metadata; a matching grid footprint alone would not establish identity. For any future altered or GEE-exported inputs, record the asset identifier, export parameters, version/date, transformations and final checksums, and cite the precise product actually used.

## Current publication scope and future extensions

The published software/synthetic archive is distinct from the private real panel. Methods and aggregate results are the chosen paper scope. There is no remaining requirement to create a full-panel dataset record. If a permitted real-data subset is separately authorised in the future, its DOI and metadata must identify that actual object. A restricted repository setting would not itself establish deposit rights. [Zenodo policies](https://about.zenodo.org/policies/)

Keep raw inputs and real company-year files outside the public repository and software archive in accordance with the author's decision. Review the actual methods/aggregate file list and required attribution before publication. No real-data licence or public full-panel availability claim is assigned.
