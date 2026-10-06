# Release readiness and archive scope

Updated 6 October 2026. Software version 0.1.0 is published on Zenodo. The manuscript and real dataset remain subject to separate review and release gates.

## Current artifacts

| Artifact | Current status | Next evidence needed |
|---|---|---|
| Software version 0.1.0 | Published software distributions, source ZIP and manifest; locally checked using synthetic inputs/tests | Preserve the frozen archive and use a new archive version for changed files |
| Maintained software repository | [Jill0099/agb-linkage-software](https://github.com/Jill0099/agb-linkage-software) is a separate public repository | Keep its software-only scope; verify each pushed revision and archive later code versions separately |
| Paper-review repository | [Jill0099/agb-linkage](https://github.com/Jill0099/agb-linkage) remains private; `v0.1.0-review` is a draft review release | Complete scientific and author review before any manuscript posting |
| Software citation | `CITATION.cff` names Yueyang Wang, Cardiff University, MIT, version 0.1.0 and the actual software DOI/date | Cite [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348) for this exact software version |
| Zenodo software metadata | [Published public-record export](zenodo_software_metadata.json), resource type software, publication date 2026-10-06 and licence identifier `mit-license` | Current record is published; the DOI resolver was verified with HTTP 200 |
| Measurement paper | Local English working draft with actual table findings, aggregate figures and pending spatial validation | Scientific gates below; final author review, disclosures and submission metadata |
| Real derived dataset | Recovered panel contains 49,022 firm-years; it remains private and has no assigned public licence or project DOI | Actual input identity, validated specification and field-specific redistribution rights |

## Published software archive

The [public record](https://zenodo.org/records/23186348) contains four files: a wheel, source distribution, software source ZIP and software manifest. The ZIP contains 42 unchanged files from original source commit `89c22458b2c4808ad6f96d70068f4b0aff7c0d46`; its SHA-256 is `5493090aa138c65e7827f43f483ec6018afd9a41bfec5688e96564ba71852e7d`. That original source commit describes the archived snapshot, not the current head of the separate public maintenance repository.

The record contains software, configurations, tests, fictitious synthetic demonstration and associated documentation. The entire paper directory, real company-year files, addresses, coordinates, provider geocoding responses and upstream rasters are excluded. The manuscript is not deposited under this DOI. Its accessible identifier can be related to the software after an actual posting exists.

A software release rests on its own evidence; it does not certify real-data validity or redistribution rights. Preparation-stage status/citation wording remains unchanged inside the frozen source files. Current repository documentation records the subsequently registered software DOI and public maintenance repository; no archived file has been rewritten.

## Published metadata and identifiers

`zenodo_software_metadata.json` reproduces the actual public-record API response saved after publication. It is a response/export, not the earlier `{"metadata": {...}}` create-request body and not a `.zenodo.json` import file. The response identifies software version 0.1.0, creator `Wang, Yueyang`, affiliation Cardiff University, open access and licence ID `mit-license`, corresponding to the MIT selection used for the actual record. Preserve the response values rather than replacing that identifier with the earlier candidate request's `mit` value. [Actual public API record](https://zenodo.org/api/records/23186348), [Zenodo API documentation](https://developers.zenodo.org/)

- Exact-version software DOI: [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348).
- All-version concept DOI: [10.5281/zenodo.23186347](https://doi.org/10.5281/zenodo.23186347).
- Publication date: 6 October 2026.
- Maintained software repository: [Jill0099/agb-linkage-software](https://github.com/Jill0099/agb-linkage-software), public.
- Paper-review repository: [Jill0099/agb-linkage](https://github.com/Jill0099/agb-linkage), private.
- No project real-data DOI, SSRN identifier or paper DOI has been created.

A future request/import file must be built for its own API/schema rather than posting this response unchanged. The response contains server-generated fields and a returned licence object. Zenodo uses `.zenodo.json` in preference to CFF for GitHub imports, so keep any later import metadata consistent. [Metadata precedence](https://help.zenodo.org/docs/github/describe-software/)

The saved export captures the remote record at the time retrieved. Its repository fields are not changed locally to anticipate a remote edit. Refresh this export only after the published record's metadata has actually been updated.

## Real-data and manuscript gates

1. Restore the user's actual annual raster inputs, establish checksums/export lineage, and confirm the actual product/version, units and scaling. Public CFATD metadata remain candidate evidence.
2. Reconcile the saved coordinates' Amap/GCJ-02 lineage with the raster reference system and independently assess placement. A new CRS label does not perform conversion.
3. Resolve forest/nonforest, valid zero, geographic background and missing coverage. The candidate source's forest-area biomass accounting does not establish that an unweighted zero-inclusive density mean is landscape biomass.
4. Complete fresh independent extraction and separately report historical reproduction and scientifically revised variants, including geometry/denominator sensitivity.
5. Inspect the applicable address and geocoding agreements for the final release fields. Removing addresses/coordinates alone does not establish permission to redistribute processed company-year observations.
6. Freeze the permitted final schema, population, version, checksums, licences, upstream citations and limitations. A dataset DOI must identify that actual released object; it cannot be substituted by the software or synthetic-example DOI.

## Author and funding information still needed

- Confirm the final creator/author list and contribution statement. Current confirmed metadata are Yueyang Wang, Cardiff University; no additional author is inferred from upstream data use or AI assistance.
- Supply a publication contact email for SSRN. A public email is not required in this software metadata; do not expose an account email without a publication decision.
- Provide ORCID only if available and verified. Its omission is not a fabricated placeholder and does not prevent basic software metadata preparation.
- Confirm funding acknowledgements and exact grant identifiers, or author-approved no-funding wording if applicable. An omitted grant field does not assert no funding.
- Confirm competing interests and any acknowledgements. Do not infer that none exist.
- Review the full manuscript, numerical evidence, citations and AI disclosure. SSRN currently requires that disclosure in both its submitted abstract and full-text PDF. [SSRN submission guidelines](https://www.elsevier.support/ssrn/answer/get-started)

## Future publication updates

The registered software identifiers are now recorded in CFF/citation instructions and the manuscript's code-availability statement. For changed software files, create a new version rather than altering the frozen ZIP. If a permitted real dataset is subsequently released, give it its own dataset record/version DOI and connect it to the paper, software and actual upstream records. Reservation precedes registration; publication creates the registered DOI. [DOI reservation](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/), [Version citations](https://zenodo.org/help/versioning)
