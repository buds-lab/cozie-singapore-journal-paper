## Cozie Singapore: Scalable crowdsourced smartwatch micro-surveys to capture longitudinal in-situ urban heat and noise perception

Public repository for the paper titled **Cozie Singapore: Scalable crowdsourced smartwatch
micro-surveys to capture longitudinal in-situ urban heat and noise perception**, using
Cozie-Apple data collected in Singapore. The analyzed dataset comprises **9,962 geolocated
micro-survey responses from 106 participants**, each pairing self-reported thermal
preference, noise, social context, and activity with the wearer's onboard physiological
signals and with linked outdoor weather and urban-form context. The deployment ran in two
phases distinguished by how just-in-time intervention (JITAI) messages were triggered; this
paper characterizes the **reported experience** across everyday urban spaces rather than the
intervention outcomes.

This public repository contains the manuscript source, the
public privacy-protected dataset, and a companion notebook that both documents the study and
regenerates every data-derived figure. It does **not** contain exact participant home
locations or the internal analysis pipeline.

## Related publications and research lineage

This paper is one output of a multi-year smartwatch deployment built on the open-source
**Cozie-Apple** platform. The publications below trace that lineage — from the first pilot
and platform description, through a public machine-learning competition on the collected
data, to the just-in-time adaptive intervention (JITAI) results. This paper characterizes
the **reported experience** across everyday urban spaces; its companion paper *Make yourself
comfortable* reports the **intervention outcomes** of the same deployment.

| Year | Publication | Role in the lineage | DOI |
|:-----|:------------|:--------------------|:----|
| 2022 | **Towards smartwatch-driven just-in-time adaptive interventions (JITAI) for building occupants** — Miller, Chua, Frei, Quintana. *BuildSys '22*, pp. 336–339. | First methods and pilot-data showcase — introduces the smartwatch-driven JITAI concept and early data. | [10.1145/3563357.3566135](https://doi.org/10.1145/3563357.3566135) |
| 2023 | **Cozie Apple: An iOS mobile and smartwatch application for environmental quality satisfaction and physiological data collection** — Tartarini, Frei, Schiavon, Chua, Miller. *J. Phys.: Conf. Ser.* **2600** 142003. | Describes the open-source data-collection platform and reports results from the first 48 participants. | [10.1088/1742-6596/2600/14/142003](https://doi.org/10.1088/1742-6596/2600/14/142003) |
| 2023 | **Introducing the Cool, Quiet City Competition: Predicting Smartwatch-Reported Heat and Noise with Digital Twin Metrics** — Miller, Quintana, Frei, Chua, Fu, Picchetti, Yap, Chong, Biljecki. *BuildSys '23*, pp. 298–299. | Launches a public (Kaggle) machine-learning competition built on this dataset. | [10.1145/3600100.3626269](https://doi.org/10.1145/3600100.3626269) |
| 2025 | **The Cool, Quiet City machine learning competition: Overview and results** — Miller, Ibrahim, Akbar, Picchetti, Chua, Frei, Biljecki, Chong, Quintana, Fu. *J. Phys.: Conf. Ser.* **3140** 112017. | Reports the design and results of that competition. | [10.1088/1742-6596/3140/11/112017](https://doi.org/10.1088/1742-6596/3140/11/112017) |
| 2025 | **Make yourself comfortable: Nudging urban heat and noise mitigation with smartwatch-based Just-in-time Adaptive Interventions (JITAI)** — Miller, Chua, Quintana, Lei, Biljecki, Frei. *Building and Environment* **284** 113388. | Reports the JITAI **intervention outcomes** of the same deployment. Has its own repository, which overlaps with this one on the participant indicator (`id_participant`): <https://github.com/buds-lab/make-yourself-comfortable-jitai-journal-paper>. | [10.1016/j.buildenv.2025.113388](https://doi.org/10.1016/j.buildenv.2025.113388) |

> **Relationship to *Make yourself comfortable*.** Both papers draw on the same participant
> cohort and can be joined on the pseudonymous `id_participant` field. This paper deliberately
> covers the *reported experience* across urban spaces, while *Make yourself comfortable*
> covers the *intervention outcomes*; the two are complementary views of one deployment.

## Requirements

Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

A LaTeX distribution with `latexmk`, `apacite`, and `natbib` is required to compile the
manuscript.

## Organization

The repository is organized into the manuscript source and three main directories:

1. [data/](./data/) <br>
   The public, privacy-protected survey dataset and its data dictionary
   ([`data/README.md`](./data/README.md)).
2. [notebooks/](./notebooks/) <br>
   The companion notebook that documents the study and regenerates the figures.
3. [figures/](./figures/) <br>
   Rendered manuscript figures (`methods/` and `data_characterization/`), with source and
   regeneration mapping in [`figures/README.md`](./figures/README.md).

Supporting files: `cozie_sg.tex` (manuscript, Taylor & Francis `interact` class),
`cozie_sg.bib` (bibliography), `tables/` (LaTeX insight tables included by the manuscript),
and the publisher template `interact.cls` with local `*.sty` dependencies.

## [Data](./data/)

The single public data file is a survey-level dataset in which each row is one smartwatch
micro-survey response joined to its pre-survey wearable-health signals, nearest-station
outdoor-weather conditions, and urban-form context.

| File | Rows × Columns | Read with |
|:-----|:---------------|:----------|
| [`data/cozie_singapore_survey_dataset.parquet.gzip`](./data/) | 9,962 × 431 | `pandas.read_parquet(..., engine='fastparquet')` |

**Privacy.** Exact home locations are **not** released. For responses reported at home
(`q_location == 'Indoor - Home'`), coordinates were spatially generalized to an
approximately 200 m hexagonal grid — a lossy, non-invertible transformation — so home
responses within the same cell share one coarsened coordinate. All non-home coordinates and
all non-coordinate fields are unchanged. None of Figures 4–15 use coordinates. Full details
are in [`data/README.md`](./data/README.md).

### Column families

| Group | Example fields | Description |
|:------|:---------------|:------------|
| Micro-survey responses | `q_thermal_preference`, `q_noise_nearby`, `q_noise_kind`, `q_earphones`, `q_location`, `q_alone_group`, `q_activity_category_alone`, `q_activity_category_group` | Watch-based survey answers. Several are conditional (answered only when reached). |
| Identifiers & timing | `id_participant`, `ws_timestamp_start`, `ws_timestamp_submit`, `ws_latitude`, `ws_longitude` | Pseudonymous participant ID, survey trigger time, survey submission time, and response coordinates (home coordinates generalized). |
| Onboard instantaneous signals | `ts_heart_rate`, `ts_oxygen_saturation`, `ts_step_count`, `ts_audio_exposure_environment`, … | Single wearable/audio values sampled at the survey moment, from the Cozie app via [Apple HealthKit](https://developer.apple.com/documentation/healthkit) (units and per-stream HealthKit links in [`data/README.md`](./data/README.md)). |
| Pre-survey wearable-health aggregates | e.g. `hr_mean_1h`, `steps_total_1h`, `walk_total_1h`, `audio_mean_1h`, `*_count_1h` | Onboard streams (heart rate, steps, walking distance, stand time, SpO₂, resting HR, ambient sound) aggregated over windows ending at the survey moment. |
| Post-survey wearable-health & weather aggregates | e.g. `hr_mean_1h_after`, `temp_mean_1h_after`, `heat_index_mean_1h_after` | The same stream/statistic summaries over windows **starting** at the survey moment (`_after` suffix). |
| Outdoor-weather aggregates | `temp_mean_1h`, `rh_mean_1h`, `heat_index_mean_1h`, `wind_speed_mean_1h`, `rain_total_1h`, `weather_station_dist_km` | Nearest-station ambient weather over the same windows, plus distance to the matched station. Source: Singapore NEA via [data.gov.sg](https://beta.data.gov.sg/collections/1459/view). Outdoor ambient, not the participant's microclimate. |
| Urban-form context (Urbanity) | `Green View Mean`, `Sky View Mean`, `Building View Mean`, `Road View Mean`, `Visual Complexity Mean`, `Building Count`, `PopSum`, POI counts (`Commercial`, `Food`, `Recreational`, …) | Built-environment indicators at each response location, computed with the [Urbanity](https://urbanity.readthedocs.io/en/latest/index.html) package ([Yap & Biljecki, Sci Data 2023](https://www.nature.com/articles/s41597-023-02578-1)). |

See [`data/README.md`](./data/README.md) for the full column dictionary — per-column units,
the exact micro-survey question wording, Apple HealthKit / NEA / Urbanity source links, and
data provenance and lineage.

#### Survey response categories

| Field | Values |
|:------|:-------|
| `q_thermal_preference` | Cooler; No change; Warmer |
| `q_noise_nearby` | None; A little; A lot |
| `q_noise_kind` *(conditional)* | Talking; Traffic; Construction; Appliances; Weather; Other |
| `q_earphones` *(conditional)* | No earphones; Earphones; Noise cancelling |
| `q_location` | Indoor - Home; Indoor - Office; Indoor - Class; Indoor - Other; Transportation; Outdoor |
| `q_location_office` *(conditional)* | Individual; Cubicles; Small shared; Large open plan; Conference room |
| `q_location_transport` *(conditional)* | Train; Bus; Car; Taxi; Other |
| `q_alone_group` | Alone; Group; Online group |
| `q_activity_category_alone` / `q_activity_category_group` *(conditional)* | Focus; Learn; Collaborate; Socialize; Leisure; Other |

#### Pre- and post-survey aggregation windows

Each wearable-health and weather stream is summarized over three windows both **before** and
**after** the survey moment (`ws_timestamp_start`):

- **Pre-survey** — `{stream}_{statistic}_{window}`, over `(start − W, start]`.
- **Post-survey** — `{stream}_{statistic}_{window}_after`, over `(start, start + W]`.

`window` is one of `10min`, `1h`, or `6h`, and `statistic` includes `count`, `mean`,
spread/extremes, and (for movement) an accumulated `total`. The **one-hour (`_1h`) window**
is the working aggregate used throughout the analysis; the six-hour window has the widest
coverage and the ten-minute window the tightest look-around. The `_after` columns are
additive (they extend the release without changing any previously published column) and are
not consumed by the manuscript figures.

`ws_timestamp_submit` records when each response was submitted, so survey completion duration
is `ws_timestamp_submit − ws_timestamp_start` (median ≈ 8.8 s). See
[`data/README.md`](./data/README.md) for the full column dictionary.

## [Notebooks](./notebooks/)

[`notebooks/cozie_singapore_companion.ipynb`](./notebooks/cozie_singapore_companion.ipynb)
is a **companion to the paper**, meant to be read alongside the manuscript. It follows the
same arc — the experiment, the micro-survey and linked data, the methods (with equations),
and the results — and regenerates Figures 4–15 directly from the public dataset. Each
section is labeled with its matching paper section, and each figure with its manuscript
number and analysis reference tag. Figure code is copied verbatim from the underlying
analysis; only the data path and figure-output target were adjusted for this repository.

Running the notebook writes each figure into `figures/data_characterization/` under its
manuscript filename, so the manuscript then compiles to the finished document:

```bash
python -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/cozie_singapore_companion.ipynb
latexmk -pdf cozie_sg.tex
```

## [Visualizations](./figures/)

The companion notebook regenerates the data-derived figures. The resulting assets live in
[`figures/data_characterization/`](./figures/data_characterization/).

| Figure | Notebook section | Output asset |
|:-------|:-----------------|:-------------|
| Figure 4  | Part 3 | [`participant_engagement.pdf`](./figures/data_characterization/participant_engagement.pdf) |
| Figure 5  | Part 3 | [`weekly_temporal_cadence.pdf`](./figures/data_characterization/weekly_temporal_cadence.pdf) |
| Figure 6  | Part 3 | [`space_type_timing_heatmaps.pdf`](./figures/data_characterization/space_type_timing_heatmaps.pdf) |
| Figure 7  | Part 4 | [`survey_battery_and_coverage.pdf`](./figures/data_characterization/survey_battery_and_coverage.pdf) |
| Figure 8  | Part 4 | [`survey_response_flow.pdf`](./figures/data_characterization/survey_response_flow.pdf) *(analytical source; manuscript uses the hand-organized `cozie-sankey-organized.png`)* |
| Figure 9  | Part 4 | [`wearable_health_windows.pdf`](./figures/data_characterization/wearable_health_windows.pdf) |
| Figure 10 | Part 4 | [`outdoor_weather_windows.pdf`](./figures/data_characterization/outdoor_weather_windows.pdf) |
| Figure 11 | Part 5 | [`cooling_preference.pdf`](./figures/data_characterization/cooling_preference.pdf) |
| Figure 12 | Part 5 | [`noise_characterization.pdf`](./figures/data_characterization/noise_characterization.pdf) |
| Figure 13 | Part 6 | [`perception_fingerprint_by_space_type.pdf`](./figures/data_characterization/perception_fingerprint_by_space_type.pdf) |
| Figure 14 | Part 6 | [`perception_lift_by_space_type.pdf`](./figures/data_characterization/perception_lift_by_space_type.pdf) |
| Figure 15 | Part 6 | [`perception_space_adjusted_residuals.pdf`](./figures/data_characterization/perception_space_adjusted_residuals.pdf) |

**Not reproduced from public data:** Figures 1–2 are hand-drawn schematics
(`figures/methods/`); Figure 3 (`response_density_and_grid_counts.png`) requires exact home
coordinates that are not part of the public release. These remain committed assets.

## Manuscript build

```bash
latexmk -pdf cozie_sg.tex
```

The generated PDF is `cozie_sg.pdf`. Temporary LaTeX build products are excluded through
`.gitignore`.

## Use of AI tools

AI assistance has been used to help structure and polish the manuscript and organize its
LaTeX source, figure assets, public dataset, and companion notebook. The authors retain
responsibility for the research, analysis, interpretation, manuscript content, and final
approval.
