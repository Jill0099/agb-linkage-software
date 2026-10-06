# Paper, GitHub, archive and citation workflow

Updated 6 October 2026. Software version 0.1.0 is publicly archived on Zenodo under [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348), with concept DOI [10.5281/zenodo.23186347](https://doi.org/10.5281/zenodo.23186347). The maintained [software-only repository](https://github.com/Jill0099/agb-linkage-software) is public. The separate [paper-review repository](https://github.com/Jill0099/agb-linkage) remains private, with a draft review release. The manuscript remains unpublished, and no project real-data DOI or SSRN posting exists.

## Research objects

| Object | What it identifies | Intended persistent record |
|---|---|---|
| Measurement paper | Scientific argument, methods, validation and bounded findings | SSRN working paper after author review and completed factual validation; possible later journal publication |
| Software | A fixed code/documentation version and synthetic demonstration | Published Zenodo version 0.1.0 software archive and a separate public maintenance repository |
| Derived observations | The exact permitted, independently validated company-year panel or explicitly named subset | Separate Zenodo dataset record with its own files, licence and version DOI |
| Upstream inputs | The actual biomass source and company/location sources used | Their original source citations and applicable rights; new project records do not replace them |

A software archive containing only code and synthetic observations must not be described as a DOI for the real matched dataset. If actual observations cannot be shared, say so in the paper and archive rather than assigning them a synthetic-data DOI.

## Dependency order

1. Freeze the historical audit and complete source identity, CRS, units, mask and independent-extraction validation. Document any corrected variant separately.
2. Resolve the exact field-level release and licences using [source rights](data_rights.md). Review authorship, funding, competing interests and the manuscript. The package may support a permissible code/documentation release before the real dataset is cleared.
3. Prepare a release manifest, checksums, paper PDF, software citation, exact input provenance and final public file list. Exclude credentials, private paths and unapproved real inputs/outputs from every archive.
4. For a cleared dataset, create a Zenodo draft and reserve its DOI when a reviewable upload is ready. Include that reserved identifier in draft files, labelling it as reserved until publication. Zenodo registers the DOI on publication. [DOI reservation](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)
5. Publish the appropriate permitted artifacts, verify the resulting landing pages and identifiers, then insert their real links in the paper and citation instructions. SSRN currently requires an English full-text PDF, author affiliations/emails and an AI disclosure in both abstract and PDF if AI is used. Its screening is not journal peer review and posting is not guaranteed. [SSRN submission requirements](https://www.elsevier.support/ssrn/answer/get-started)
6. Check the published paper, repository and dataset metadata against the same frozen versions. Record their relationships and test the generated citations. Add a real paper citation to `preferred-citation` only after an accessible paper exists.

There is no mandatory universal posting order between software, paper and dataset. The dependency is truthful, reviewable content and accurate identifiers. A dataset DOI may be reserved before a paper is posted so the paper can identify the intended record; it must not be presented as a published data record until publication.

## Citation/version rules

Use the exact version DOI when reporting empirical inputs or a software version. The concept DOI represents the evolving record and resolves to its latest version. New files require a new archive version; a metadata-only correction can retain the existing version DOI. [Zenodo versioning](https://zenodo.org/help/versioning)

`CITATION.cff` provides software metadata without fabricated identifiers. Keep `CITATION.md` explicit about software, paper, derived data and upstream citations. If `.zenodo.json` is later added for GitHub release imports, it overrides the CFF metadata on Zenodo, so verify consistency before each release. [Zenodo metadata precedence](https://help.zenodo.org/docs/github/describe-software/), [GitHub citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)

DOIs and citation instructions aid attribution and reproducibility. They do not enforce a two-citation rule, confer redistribution rights, establish journal acceptance or guarantee indexing/citation counts.

The [published software metadata export](zenodo_software_metadata.json) and [release-readiness record](release_readiness.md) identify the actual software record and remaining dataset/manuscript decisions. The JSON reproduces the public record response, rather than the earlier create-request draft; refresh it only after an actual remote metadata change. The published archive excludes the entire paper directory and real-data inputs/outputs; its original source commit is `89c22458b2c4808ad6f96d70068f4b0aff7c0d46`, distinct from the separate public maintenance repository's current head. Preparation-stage statements inside the frozen archive describe that source snapshot and have not been rewritten after publication. Later maintained code must receive its own archived version before it is cited as a fixed research input.
