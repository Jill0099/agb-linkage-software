# Data rights and release boundaries

Checked 6 October 2026. This document records evidence and release decisions; it does not establish the terms of an institutional contract that has not been inspected.

The project contributes company-location linkage and extraction methods. The source AGB rasters, company-address records, and geocoding responses have separate provenance and rights. A licence on the new software does not license those inputs or all derived tables.

## Evidence matrix

| Material | Evidence checked | Current decision | Evidence needed to clear a real-data release |
|---|---|---|---|
| New `agb-linkage` software | New implementation prepared for this project | MIT applies to the project's original software as specified in the root licence; no third-party data rights are granted | Confirm any incorporated third-party code and contributor ownership |
| Candidate CFATD annual rasters | Six public Zenodo API records report `cc-by-4.0`, open access; record IDs and file MD5 checksums are in `upstream_candidates.json` | Candidate product has an identified open licence; actual input identity is still unconfirmed | Match recovered files to provider checksums or document the actual export/version; retain attribution and licence/change notices |
| Company identifiers and office-address histories | Historical project documentation names CSMAR; export table/version and the applicable institution agreement are unavailable | Keep original exports and linked observations out of public packages pending a specific decision | Obtain the agreement covering the actual export; establish rights for identifiers, addresses, matching outputs, and processed observations |
| Amap geocodes and quality fields | Original scripts parse Amap outputs; current provider terms and coordinate documentation checked | No open licence for the saved responses has been established; keep them private | Verify the account/product terms applicable when acquired and now, or obtain written permission covering coordinate/derived-data dissemination |
| Real company-year AGB linkage | Combines the preceding inputs; audit confirms 49,022 observations in the recovered research panel | No public data licence assigned; no assertion that removing address/coordinate columns alone clears redistribution | Assess the proposed final fields and intended use against every applicable input agreement |
| Synthetic demonstration | Artificial raster and fictitious location identifiers generated for demonstrating the software | Can be prepared without distributing real provider responses or listed-company observations | Verify documentation clearly identifies it as synthetic and checksums identify only this demonstration |
| Paper and aggregate audit summaries | Manuscript describes methods and tabular findings without row-level firm/address/coordinate records | Local review draft; neither SSRN-posted nor submission-ready | Complete scientific validation, authorship/disclosure review, and any applicable restrictions on reported information |

## What the provider documents actually say

All six candidate CFATD Zenodo records report the licence identifier `cc-by-4.0` in their public metadata. This confirms the records' listed licence, not the identity of the user's inputs. [Part I](https://zenodo.org/api/records/12620984), [Part II](https://zenodo.org/api/records/12637101), [Part III](https://zenodo.org/api/records/12655492), [Part IV](https://zenodo.org/api/records/12658255), [Part V](https://zenodo.org/api/records/12742210), [Part VI](https://zenodo.org/api/records/12747329)

CC-BY-4.0 permits sharing and adaptation subject to attribution, a licence link, and indicating changes; it does not remove rights associated with unrelated inputs. For a cleared derivative, identify the AGB authors/product/version, explain the new matching and aggregation, and preserve the source licence information. [Creative Commons licence deed](https://creativecommons.org/licenses/by/4.0/)

Amap's current platform service terms were updated on 3 December 2025. Section 2.2 expressly includes geocoding, coordinates and address data among covered content. Section 4.12 describes restrictions, subject to its stated legal/permission conditions, on copying, derivative works/databases, standalone display and dissemination. These clauses warrant checking the precise account/product agreement and intended derived output. They are not a finding that the user's historical research was unauthorised. Collection logs precede this revision, so the terms applicable to that collection also need verification. [Amap service terms](https://lbs.amap.com/pages/terms/)

A publicly posted CSMAR supplier contract at Tianjin University addresses provision of both database content and processed data to third parties. It is useful evidence that derivative rights can be contract-specific, but it is not the agreement applicable to this project. The provider's public product page describes research and custom-data services without granting a general redistribution licence. [Public supplier-contract example](https://zbb.tju.edu.cn/sfw_cms/r/s/cms/392c81330d28410fb357ba74080b6462/0/CSMAR%E6%95%B0%E6%8D%AE%E5%BA%93%E5%90%88%E5%90%8C.pdf), [CSMAR product information](https://www.csmar.com/channels/31.html)

## Concrete decisions to resolve

For CSMAR, identify the original company-information table, export date, subscriber institution and agreement. Ask the relevant rightsholder or institutional data service to assess the intended release schema: stock identifier, year, location-quality flags, and biomass summary statistics; assess raw address and coordinate sharing separately. Preserve the actual response or agreement rather than recording a generic “permission obtained” status.

For Amap, identify the account/product and collection period. Determine whether saved coordinates, provider quality fields, coordinate transformations and third-party-raster summaries may be distributed under the applicable terms. If permission is unavailable, a separately sourced location reconstruction would need its own provenance and validation; changing a licence label or deleting coordinates does not establish that reconstruction.

For the raster product, compare actual annual file names, size and hashes to `upstream_candidates.json`. A matching grid footprint is supporting evidence, not a hash match. If the files were exported from GEE or altered, record the public asset identifier, export parameters, version/date, transformations and final checksums. Cite the precise product actually used.

## Publication paths

A code/documentation release with a synthetic example is distinct from a public full-panel dataset. If only that package is cleared, use software metadata and describe the real panel as unavailable. If a permitted subset is released, its DOI and metadata must explicitly identify the subset. A restricted-access repository setting does not itself establish deposit rights: Zenodo permits uploads only where appropriate rights exist. [Zenodo policies](https://about.zenodo.org/policies/)

Keep raw inputs and real company-year files outside the public repository and software archive until field-specific decisions are documented. Before publication, complete the chosen release's rights matrix with actual evidence, final field list, licence allocation and required attribution. No real-data licence or public-data availability claim is assigned by this draft.
