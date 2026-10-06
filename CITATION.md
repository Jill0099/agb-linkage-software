# Citation and attribution instructions

**Current status:** software version 0.1.0 was published on Zenodo on 6 October 2026 under [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348). The maintained [software-only GitHub repository](https://github.com/Jill0099/agb-linkage-software) is public. The separate [paper-review repository](https://github.com/Jill0099/agb-linkage) remains private, with a draft review release. The measurement-paper manuscript remains unpublished. No SSRN paper identifier, journal DOI or project derived-dataset DOI exists. No real company-year panel is publicly released.

## Cite what you actually use

- **Software:** cite Yueyang Wang, the title in `CITATION.cff`, version 0.1.0, year 2026 and the registered [software version DOI](https://doi.org/10.5281/zenodo.23186348). The [public software repository](https://github.com/Jill0099/agb-linkage-software) is the maintenance location; the DOI identifies the fixed archive used in research.
- **Method or measurement paper:** use the genuine SSRN working-paper citation after posting, clearly labelled as a working paper/preprint. After journal publication, use the appropriate published-paper metadata. Do not invent a paper DOI or label this local draft as a peer-reviewed article.
- **Released observations:** cite the derived dataset's exact version DOI and the linkage paper where relevant after an actual data release. A software or synthetic-example DOI does not identify the unreleased real panel.
- **Upstream AGB:** cite the exact source dataset record(s) and associated paper used in the matching, retain required attribution/licence notices, and describe the linkage/aggregation changes. The matching authors did not create the source raster estimates.
- **Company and coordinate inputs:** comply separately with source-agreement attribution and redistribution conditions. A source citation alone does not establish permission to share its data.

Suggested manuscript title is *Local Aboveground Biomass around Chinese Listed-Company Office Locations: A Geospatial Matching and Measurement Audit*. Current author information is Yueyang Wang, Cardiff University; ORCID and publication email have not been supplied. Confirm the final author list and title before public posting.

## Software citation

Wang, Y. (2026). *agb-linkage: Chinese listed-company location and biomass linkage tools* (Version 0.1.0) [Software]. Zenodo. [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348).

Use the version DOI above for the fixed software used in research. The [concept DOI, 10.5281/zenodo.23186347](https://doi.org/10.5281/zenodo.23186347), represents all versions and resolves to the latest version. The software archive excludes the manuscript and real company-year observations. It does not replace their future paper or dataset citations.

```bibtex
@software{wang2026agblinkage,
  author       = {Wang, Yueyang},
  title        = {agb-linkage: Chinese listed-company location and biomass linkage tools},
  year         = {2026},
  version      = {0.1.0},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.23186348},
  url          = {https://doi.org/10.5281/zenodo.23186348},
  note         = {Software archive with synthetic examples; real company-year data and manuscript excluded.}
}
```

BibLaTeX supports `@software`; a BibTeX style without that entry type can use `@misc` with the same fields.

The published source archive is frozen at original source commit `89c22458b2c4808ad6f96d70068f4b0aff7c0d46`. That commit identifies the archived source snapshot, rather than the current head of the separate public maintenance repository. Preparation-stage citation/status text is retained unchanged within the frozen files; the current citation above identifies the subsequently registered software record. Cite a newly archived version if later maintained code is used instead of this snapshot.

## Candidate upstream citations — verify input identity first

CFATD is a researched candidate source, not yet a confirmed match to the recovered input files. Its published source paper is:

Cai, Y., et al. (2025). *Dynamics of China's forest carbon storage: the first 30 m annual aboveground biomass mapping from 1985 to 2023*. Earth System Science Data, 17, 6993–7018. [https://doi.org/10.5194/essd-17-6993-2025](https://essd.copernicus.org/articles/17/6993/2025/).

If actual inputs are confirmed as this product, cite the applicable archive parts using each record's creators, title, metadata publication date and exact DOI. The recovered 2007–2022 research panel would span Parts III–VI; a wider 2000–2023 rebuild would also use Part II. Part I should not be cited as an input merely because it is the first archive page.

| Candidate part | Years | Actual data-record DOI |
|---|---|---|
| I | 1985–1993 | [10.5281/zenodo.12620984](https://zenodo.org/records/12620984) |
| II | 1994–2001 | [10.5281/zenodo.12637101](https://zenodo.org/records/12637101) |
| III | 2002–2008 | [10.5281/zenodo.12655492](https://zenodo.org/records/12655492) |
| IV | 2009–2015 | [10.5281/zenodo.12658255](https://zenodo.org/records/12658255) |
| V | 2016–2021 | [10.5281/zenodo.12742210](https://zenodo.org/records/12742210) |
| VI | 2022–2023 | [10.5281/zenodo.12747329](https://zenodo.org/records/12747329) |

The archive API metadata currently gives July 2024 publication dates, whereas the source paper labels its dataset references 2025. Use the record metadata consistently rather than silently assigning the paper's year to the dataset. The final source-paper DOI above is distinct from the older discussion-preprint DOI still appearing in some archive descriptions. See [provenance](docs/provenance.md).

## Populate identifiers during the release stage

Zenodo permits reserving a DOI in a draft to include inside files; it is registered when the record is published. Use version DOIs for fixed empirical inputs and the concept DOI for the evolving project. The latter resolves to the latest version. [Zenodo DOI reservation](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/), [DOI versioning](https://zenodo.org/help/versioning)

Once a genuine paper identifier exists, update `preferred-citation` in `CITATION.cff` using accurate status and metadata, while keeping the data/software version citations visible here. If a `.zenodo.json` file is later supplied, keep it consistent with the CFF: Zenodo gives that JSON precedence for imported GitHub releases. [GitHub citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files), [Zenodo metadata precedence](https://help.zenodo.org/docs/github/describe-software/)

These instructions support attribution and reproducibility. They do not guarantee scholarly citation or search-engine indexing, and they do not transfer ownership of upstream data.
