# Release readiness and archive scope

Updated 6 October 2026. Software version 0.1.0 is published on Zenodo. SSRN received the author-reviewed working paper as Abstract ID 7570918; screening is pending, and real observations stay private by author choice.

The author's selected scope is methods and aggregate findings, with real observations kept private. A full-panel public data release and project dataset DOI are outside the current deliverables.

## Current artifacts

| Artifact | Current status | Next evidence needed |
|---|---|---|
| Software version 0.1.0 | Published software distributions, source ZIP and manifest; locally checked using synthetic inputs/tests | Preserve the frozen archive and use a new archive version for changed files |
| Maintained software repository | [Jill0099/agb-linkage-software](https://github.com/Jill0099/agb-linkage-software) is a separate public repository | Keep its software-only scope; verify each pushed revision and archive later code versions separately |
| Paper-review repository | [Jill0099/agb-linkage](https://github.com/Jill0099/agb-linkage) remains private; `v0.1.0-review` is a draft review release | Preserve historical review assets; final author-reviewed PDF has been submitted to SSRN |
| Software citation | `CITATION.cff` names Yueyang Wang, Cardiff University, MIT, version 0.1.0 and the actual software DOI/date | Cite [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348) for this exact software version |
| Zenodo software metadata | [Published-record metadata snapshot](zenodo_software_metadata.json), retrieved 6 October 2026 after the public-repository metadata update; resource type software and licence identifier `mit-license` | The coordinator's subsequent public read confirms the same published description, DOI/version and four file checksums; the new source-audit description remains a draft |
| Measurement paper | [SSRN 7570918](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7570918), receipt verified; 11-page author-reviewed preprint, CC BY 4.0 | Await SSRN screening; retain coordinate/mask limits and verify any later paper DOI from actual metadata |
| Real derived dataset | Recovered panel contains 49,022 firm-years and remains private by author choice | Public dataset release is not a current deliverable; a separately authorised future release would require scientific and field-specific rights evidence |

## Published software archive

The [public record](https://zenodo.org/records/23186348) contains four files: a wheel, source distribution, software source ZIP and software manifest. The ZIP contains 42 unchanged files from original source commit `89c22458b2c4808ad6f96d70068f4b0aff7c0d46`; its SHA-256 is `5493090aa138c65e7827f43f483ec6018afd9a41bfec5688e96564ba71852e7d`. That original source commit describes the archived snapshot, not the current head of the separate public maintenance repository.

The record contains software, configurations, tests, fictitious synthetic demonstration and associated documentation. The entire paper directory, real company-year files, addresses, coordinates, provider geocoding responses and upstream rasters are excluded. The manuscript is not deposited under this DOI. Its accessible identifier can be related to the software after an actual posting exists.

A software release rests on its own evidence; it does not certify real-data validity or redistribution rights. Preparation-stage status/citation wording remains unchanged inside the frozen source files. Current repository documentation records the subsequently registered software DOI and public maintenance repository; no archived file has been rewritten.

## Published metadata and identifiers

`zenodo_software_metadata.json` preserves a published-record API snapshot retrieved on 6 October 2026 after the public-repository metadata update. It is a response/export, not the earlier `{"metadata": {...}}` create-request body and not a `.zenodo.json` import file. The response identifies software version 0.1.0, creator `Wang, Yueyang`, affiliation Cardiff University, open access and licence ID `mit-license`, corresponding to the MIT selection used for the actual record. Preserve the response values rather than replacing that identifier with the earlier candidate request's `mit` value. [Actual public API record](https://zenodo.org/api/records/23186348), [Zenodo API documentation](https://developers.zenodo.org/)

- Exact-version software DOI: [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348).
- All-version concept DOI: [10.5281/zenodo.23186347](https://doi.org/10.5281/zenodo.23186347).
- Publication date: 6 October 2026.
- Maintained software repository: [Jill0099/agb-linkage-software](https://github.com/Jill0099/agb-linkage-software), public.
- Paper-review repository: [Jill0099/agb-linkage](https://github.com/Jill0099/agb-linkage), private.
- SSRN Abstract ID: [7570918](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7570918), submission received 6 October 2026; screening pending.
- No project real-data DOI or paper DOI is claimed.

A future request/import file must be built for its own API/schema rather than posting this response unchanged. The response contains server-generated fields and a returned licence object. Zenodo uses `.zenodo.json` in preference to CFF for GitHub imports, so keep any later import metadata consistent. [Metadata precedence](https://help.zenodo.org/docs/github/describe-software/)

The saved snapshot captures published metadata rather than live statistics. The coordinator's public read on 6 October 2026 at 12:24 UTC confirms that its description, software DOI/version and four file checksums still match the published record. A verified description update incorporating the completed source audit has been prepared as a reversible Zenodo draft; that description update has not been published. Published-record exports remain distinct from this draft. No export fields are changed locally to anticipate a remote edit; a refreshed export must reflect an actual published API response.

## Current manuscript checks and separately scoped extensions

1. All 16 research-panel inputs from 2007–2022 match official CFATD Parts III–VI sizes and complete MD5s, with each file unchanged during its read. Native encoding and fresh reproduction on the preserved 200 cases are checked. This confirms only the 16 panel-year rasters, not all 39 restored files. See [source-file verification](source_file_verification.json).
2. State the documented direct Amap-response parsing, unchanged panel coordinates and unreconciled GCJ-02/EPSG:4326 lineage. Independent placement and a corrected transformation would be scientific extensions; do not imply they are completed.
3. State unresolved forest/nonforest, valid zero, geographic background and missing coverage. The provider's forest-area biomass accounting does not establish that the historical unweighted zero-inclusive mean is landscape biomass.
4. Report the fresh numerical check accurately: 200 exact points and 600 serialized means/counts from the preserved list, without a random/representative geographic validation claim. Corrected coordinate, geometry and mask variants require their own future validation.
5. Review the methods/aggregate publication file list and any applicable restrictions on the information reported. Real observations, addresses and coordinates remain excluded by author choice.
6. Finalise the audit population, source/version citations, software citation, limitations and author-approved text. No project real-data DOI is required for this scope.

## Confirmed author information and submission

Yueyang Wang, Cardiff University, confirmed PDF review, upload rights, agreement to SSRN terms, no specific research funding, no competing interests and CC BY 4.0. The author-supplied email is recorded in the paper/private submission metadata; the public software citation need not reproduce it. AI assistance is disclosed in the PDF and submitted abstract. Upstream creators remain credited separately.

The 11-page final PDF was uploaded to the existing SSRN draft; extracted title/abstract were corrected and reviewed, the paper date is 6 October 2026, and Environmental Studies was selected. Required funding and interest statements were supplied. Terms were accepted and the licence selected only after explicit author confirmation. SSRN returned “Your submission has been received” and Abstract ID 7570918. Its abstract page loads in the verified browser session with the expected declarations and CC BY 4.0. Anonymous access and a paper DOI are not independently verified, and SSRN screening remains pending.

The private repository contains the concrete submission metadata and checklist; the paper directory is excluded from the public software repository. Coordinate and ecological improvements remain explicitly limited scientific extensions. The saved Zenodo source-audit description remains a separate unpublished draft awaiting its own approval; its four software files and registered DOI are unchanged.

## Future publication updates

The registered software identifiers are now recorded in CFF/citation instructions and the manuscript's code-availability statement. For changed software files, create a new version rather than altering the frozen ZIP. If a permitted real dataset is subsequently released, give it its own dataset record/version DOI and connect it to the paper, software and actual upstream records. Reservation precedes registration; publication creates the registered DOI. [DOI reservation](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/), [Version citations](https://zenodo.org/help/versioning)
