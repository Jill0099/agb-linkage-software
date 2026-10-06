# Citation and attribution instructions

**Current status:** software version 0.1.0 was published on Zenodo on 6 October 2026 under [10.5281/zenodo.23186348](https://doi.org/10.5281/zenodo.23186348). The maintained [software-only GitHub repository](https://github.com/Jill0099/agb-linkage-software) is public. The separate [paper-review repository](https://github.com/Jill0099/agb-linkage) remains private, with historical draft review releases. SSRN received the author-reviewed measurement paper on 6 October 2026 as [Abstract ID 7570918](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7570918); its abstract page loads in the verified browser session, while screening remains pending. The paper uses CC BY 4.0. No paper DOI, journal acceptance or project derived-dataset DOI is claimed. No real company-year panel is publicly released.

## Cite what you actually use

- **Software:** cite Yueyang Wang, the title in `CITATION.cff`, version 0.1.0, year 2026 and the registered [software version DOI](https://doi.org/10.5281/zenodo.23186348). The [public software repository](https://github.com/Jill0099/agb-linkage-software) is the maintenance location; the DOI identifies the fixed archive used in research.
- **Method or measurement paper:** use the genuine SSRN working-paper citation below, clearly labelled as a working paper/preprint whose screening remains pending. After journal publication, use the appropriate published-paper metadata. Do not invent a paper DOI or label this working paper as a peer-reviewed article.
- **Released observations:** cite the derived dataset's exact version DOI and the linkage paper where relevant after an actual data release. A software or synthetic-example DOI does not identify the unreleased real panel.
- **Upstream AGB:** cite the exact source dataset record(s) and associated paper used in the matching, retain required attribution/licence notices, and describe the linkage/aggregation changes. The matching authors did not create the source raster estimates.
- **Company and coordinate inputs:** comply separately with source-agreement attribution and redistribution conditions. A source citation alone does not establish permission to share its data.

The submitted title is *Local Aboveground Biomass around Chinese Listed-Company Office Locations: A Geospatial Matching and Measurement Audit*. The listed author is Yueyang Wang, Cardiff University. The author confirmed PDF review, upload rights, no specific funding, no competing interests and CC BY 4.0; the contact email is recorded in the paper and private submission metadata.

The author has chosen to publish methods and aggregate findings while keeping real observations private. A real-panel dataset DOI is not required by the current scope. The released-observation instruction above applies only to a separately authorised future data release.

## Working-paper citation

Wang, Y. (2026). *Local Aboveground Biomass around Chinese Listed-Company Office Locations: A Geospatial Matching and Measurement Audit*. Working paper/preprint, SSRN Abstract ID 7570918. [SSRN paper page](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7570918).

SSRN confirmed submission receipt on 6 October 2026. Screening remains pending; the paper is not represented as journal peer reviewed or accepted. No paper DOI was displayed in the verified page. Use the actual SSRN URL and identifier rather than constructing a DOI from the abstract number.

```bibtex
@misc{wang2026agbmeasurement,
  author = {Wang, Yueyang},
  title  = {Local Aboveground Biomass around Chinese Listed-Company Office Locations: A Geospatial Matching and Measurement Audit},
  year   = {2026},
  url    = {https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7570918},
  note   = {Working paper/preprint. SSRN Abstract ID 7570918; submission received 6 October 2026, screening pending.}
}
```

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

## Confirmed upstream inputs and citations

Complete file sizes and MD5s identify all 16 annual research-panel inputs for 2007–2022 as CFATD Parts III–VI. Each input was unchanged during its read. This confirms those 16 files, not all 39 rasters in the restored collection. See the [source-file verification](docs/source_file_verification.json) and [provenance](docs/provenance.md).

Cite the source article separately from the data records:

Cai, Y., et al. (2025). *Dynamics of China's forest carbon storage: the first 30 m annual aboveground biomass mapping from 1985 to 2023*. Earth System Science Data, 17, 6993–7018. [10.5194/essd-17-6993-2025](https://essd.copernicus.org/articles/17/6993/2025/).

The official dataset exports list these creators: Cai, Yaotong; Zhu, Peng; Xu, Xiaocong; Li, Xing; Zhang, Honghui; Nie, Sheng; Wang, Cheng; Wang, Jia; Shen, Qianhui; Li, Bingjie; Wu, Changjiang; Liu, Xiaoping; Chen, Yuhe. Cite the actual records below, preserving their titles, publication dates and creator metadata. Dataset authorship differs from the final article's author list.

| Confirmed record title | Panel years used | Record publication date | Exact data-record DOI |
|---|---|---|---|
| *CFATD: The First High-Spatiotemporal-Resolution Mapping of Forest Aboveground Biomass in China from 1985 to 2023 (Part Ⅲ: 2002-2008)* | 2007–2008 | 4 July 2024 | [10.5281/zenodo.12655492](https://zenodo.org/records/12655492) |
| *CFATD: The First High-Spatiotemporal-Resolution Mapping of Forest Aboveground Biomass in China from 1985 to 2023 (Part Ⅳ: 2009-2015)* | 2009–2015 | 4 July 2024 | [10.5281/zenodo.12658255](https://zenodo.org/records/12658255) |
| *CFATD: The First High-Spatiotemporal-Resolution Mapping of Forest Aboveground Biomass in China from 1985 to 2023 (Part Ⅴ: 2016-2021)* | 2016–2021 | 15 July 2024 | [10.5281/zenodo.12742210](https://zenodo.org/records/12742210) |
| *CFATD: The First High-Spatiotemporal-Resolution Mapping of Forest Aboveground Biomass in China from 1985 to 2023 (Part Ⅵ: 2022-2023)* | 2022 | 16 July 2024 | [10.5281/zenodo.12747329](https://zenodo.org/records/12747329) |

The archive metadata and official BibTeX exports give July 2024 publication dates, whereas the source paper labels its dataset references 2025. Use the data-record metadata consistently rather than assigning the paper's year to the dataset. The final source-paper DOI above is distinct from the older discussion-preprint DOI still appearing in some archive descriptions. Parts I and II are not inputs to the current 2007–2022 panel.

These records list [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). Retain attribution and licence information and describe the company-location matching, square aggregation and zero-inclusion convention as project changes. Provider-documented forest density units are Mg/ha with native scale 1 and offset 0. File identity and numerical reproduction do not establish the historical coordinates' reference-system reconciliation or the ecological validity of zero/mask denominators.

## Populate identifiers during the release stage

Zenodo permits reserving a DOI in a draft to include inside files; it is registered when the record is published. Use version DOIs for fixed empirical inputs and the concept DOI for the evolving project. The latter resolves to the latest version. [Zenodo DOI reservation](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/), [DOI versioning](https://zenodo.org/help/versioning)

Once a genuine paper identifier exists, update `preferred-citation` in `CITATION.cff` using accurate status and metadata, while keeping the data/software version citations visible here. If a `.zenodo.json` file is later supplied, keep it consistent with the CFF: Zenodo gives that JSON precedence for imported GitHub releases. [GitHub citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files), [Zenodo metadata precedence](https://help.zenodo.org/docs/github/describe-software/)

These instructions support attribution and reproducibility. They do not guarantee scholarly citation or search-engine indexing, and they do not transfer ownership of upstream data.
