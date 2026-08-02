# Public data — Cozie Singapore

This folder contains the **public, privacy-protected** survey dataset accompanying the
Cozie Singapore manuscript. It is sufficient to reproduce manuscript **Figures 4-15** via
the companion notebook
[`../notebooks/cozie_singapore_companion.ipynb`](../notebooks/cozie_singapore_companion.ipynb).

## File

| File | Description |
|---|---|
| `cozie_singapore_survey_dataset.parquet.gzip` | Survey-level dataset, gzip-compressed Parquet. Read with `pandas.read_parquet(..., engine='fastparquet')`. |

- **Size:** 9,962 survey responses × 431 columns, from 106 participants.
- Each row is one smartwatch micro-survey response, joined to the wearable-health signals,
  nearest-station outdoor-weather conditions, and urban-form context for that response.
- Wearable-health and weather signals are summarized both **before** the survey (pre-survey
  look-back windows) and **after** it (post-survey look-ahead windows, `_after` suffix).

## Source platforms & lineage

**Cozie smartwatch platform.** Micro-survey responses and the physiological / environmental /
activity streams were collected with the [Cozie](https://cozie-apple.app/) Apple Watch app.
Two broad families come from the watch: **micro-survey data** (the `q_*` responses plus
`ws_*` context) and **physiological / activity / environmental data** (the `ts_*` streams,
sourced from Apple HealthKit — see section C).

**Source export is sparse; this release is dense.** In the raw Cozie export there is one row
per sample, so physiological/environmental rows (sampled at higher frequency than surveys)
vastly outnumber survey rows and the survey columns are mostly empty — only rows with a
micro-survey response carry an integer `ws_survey_count`, the `q_*` answers, and
coordinates. In the source data, common filters were therefore needed, e.g.:

```python
# One participant's micro-survey responses (source Cozie export)
mask = (df['id_participant'] == 'xesh001') & (df['ws_survey_count'].notna())
```

**This public dataset is already survey-level and dense:** every row is one micro-survey
response with its aggregated wearable/weather/urban-form context joined on, so no
survey-vs-sample filtering is required here (`ws_survey_count` is populated on every row, and
all rows carry valid coordinates). To subset one participant, filter on `id_participant`
alone. This dataset also omits the source export's `id_unique` and `index` columns; the
submission timestamp that served as `index` is provided explicitly as `ws_timestamp_submit`.

**Lineage.** The dataset and this dictionary extend the earlier public release prepared for
the **Cool Quiet City** competition; column semantics, source links, and the ~200 m home
generalization approach are inherited from that release (this version implements the home
generalization in the SVY21 / EPSG:3414 projection — see Privacy). It adds the QC-gated
pre-/post-survey aggregation windows and `ws_timestamp_submit`.

## Data categories

The 431 columns fall into eight groups:

| # | Category | Approx. count | What it captures |
|---|---|---|---|
| A | Response identifiers & timing | 8 | Participant ID, survey trigger/submission/location timestamps, response counter. |
| B | Micro-survey responses (`q_*`) | 10 | The watch-based survey answers (thermal, noise, location, social context, activity). |
| C | Onboard instantaneous signals (`ts_*`) | 7 | Health/audio values at the survey moment (heart rate, SpO₂, steps, etc.). |
| D | Weather-station link | 2 | Nearest government station matched to the response and its distance. |
| E | Temporal features | 4 | Hour, day-of-week, weekend flag, month derived from the survey time. |
| F | Urban-form context (Urbanity) | 32 | Building morphology, population, points-of-interest, and streetscape view indices at the location. |
| G | Pre-survey wearable/weather aggregates | 186 | `{stream}_{statistic}_{window}` summaries over windows **ending** at the survey moment. |
| H | Post-survey wearable/weather aggregates (`_after`) | 180 | The same stream/statistic summaries over windows **starting** at the survey moment. |

## Column dictionary

### A · Response identifiers & timing

| Column | Type | Unit | Description |
|---|---|---|---|
| `id_participant` | string | – | Unique, pseudonymous identifier for each participant (no direct identity). |
| `ws_timestamp_start` | datetime (UTC) | time | Timestamp of when the micro-survey was started — "the survey moment". Anchors every pre- and post-survey aggregation window. |
| `ws_timestamp_submit` | datetime (UTC) | time | Timestamp of when the micro-survey was submitted. In the source Cozie export this is the row `index`. Survey completion duration = `ws_timestamp_submit − ws_timestamp_start` (median ≈ 8.8 s; see notes). |
| `ws_timestamp_location` | datetime (UTC) | time | Timestamp of the location measurement. Usually close to `ws_timestamp_submit`, but can be substantially older when the device reused an earlier location fix. |
| `ws_latitude`, `ws_longitude` | float | ° | Response latitude / longitude (WGS84). Home responses are spatially generalized (see Privacy). |
| `ws_survey_count` | float | – | Increasing counter for each micro-survey response; resets when the Cozie app is (re-)installed. |
| `dT` | float | min | Duration between the current and the previous micro-survey response. (Responses < 55 min apart were removed upstream, so the minimum observed value is ≈ 55.) |
| `end` | string | – | Survey terminal-action marker (`"Submit survey"`). |

### B · Micro-survey responses (`q_*`)

All response columns carry the `q_` prefix. The "Survey question" column gives the exact
prompt shown on the watch.

| Column | Type | Survey question | Description |
|---|---|---|---|
| `q_thermal_preference` | string | *Thermally, what do you prefer now?* | Desired change in thermal condition. |
| `q_noise_nearby` | string | *Noise distractions nearby? (without earphones)* | Perceived amount of nearby noise. |
| `q_noise_kind` | string | *What kind of noise?* | Dominant noise source *(conditional — asked only when noise is reported)*. |
| `q_earphones` | string | *Wearing earphones?* | Earphone use at the time of response *(conditional)*. |
| `q_location` | string | *Where are you?* | Reported space type. |
| `q_location_office` | string | *What kind of office?* | Office sub-type *(conditional on an office location)*. |
| `q_location_transport` | string | *What kind of transport?* | Transport mode *(conditional on a transport location)*. |
| `q_alone_group` | string | *Alone or in a group?* | Social context (alone / group / online group). |
| `q_activity_category_alone` | string | *Category of activity? (alone)* | Activity when alone *(conditional)*. |
| `q_activity_category_group` | string | *Category of activity? (group)* | Activity when in a group *(conditional)*. |

Response categories:

| Field | Values |
|---|---|
| `q_thermal_preference` | Cooler; No change; Warmer |
| `q_noise_nearby` | None; A little; A lot |
| `q_noise_kind` *(conditional)* | Talking; Traffic; Construction; Appliances; Weather; Other |
| `q_earphones` *(conditional)* | No earphones; Earphones; Noise cancelling |
| `q_location` | Indoor - Home; Indoor - Office; Indoor - Class; Indoor - Other; Transportation; Outdoor |
| `q_location_office` *(conditional)* | Individual; Cubicles; Small shared; Large open plan; Conference room |
| `q_location_transport` *(conditional)* | Train; Bus; Car; Taxi; Other |
| `q_alone_group` | Alone; Group; Online group |
| `q_activity_category_alone` / `q_activity_category_group` *(conditional)* | Focus; Learn; Collaborate; Socialize; Leisure; Other |

### C · Onboard instantaneous signals (`ts_*`)

Single wearable/audio values attached to the response moment (as opposed to the windowed
aggregates in groups G/H). All `ts_*` streams originate from the Cozie app via **Apple
HealthKit**. On the source platform these are sampled independently of the micro-survey and
at intervals that differ between streams (and may change within a stream); in this
survey-level release each value is the sample carried on the response row.

| Column | Type | Unit | Source (Apple HealthKit) |
|---|---|---|---|
| `ts_heart_rate` | float | bpm | [`heartRate`](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/1615138-heartrate) |
| `ts_resting_heart_rate` | float | bpm | [`restingHeartRate`](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/2867756-restingheartrate) |
| `ts_oxygen_saturation` | float | % | [`oxygenSaturation`](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/1615377-oxygensaturation) (blood oxygen, SpO₂) |
| `ts_step_count` | float | steps | [`stepCount`](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/1615548-stepcount) (timestamp marks the first step in the sample) |
| `ts_walking_distance` | float | m | [`distanceWalkingRunning`](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/1615230-distancewalkingrunning) |
| `ts_stand_time` | float | min | [`appleStandTime`](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/3174858-applestandtime) |
| `ts_audio_exposure_environment` | float | dB(A) | [`environmentalAudioExposure`](https://developer.apple.com/documentation/healthkit/hkquantitytypeidentifier/3081271-environmentalaudioexposure) |

### D · Weather-station link

| Column | Type | Description |
|---|---|---|
| `weather_station_id` | string | ID of the nearest government weather station matched to the response. |
| `weather_station_dist_km` | float | Distance from the response location to that station (km). |

### E · Temporal features

Derived from `ws_timestamp_start` (Singapore local time).

| Column | Type | Description |
|---|---|---|
| `hour_of_day` | int | Hour of day (0–23). |
| `day_of_week` | int | Day of week (0 = Monday). |
| `is_weekend` | int | 1 if Saturday/Sunday, else 0. |
| `month` | int | Calendar month (1–12). |

### F · Urban-form context (Urbanity)

Built-environment indicators at each response location, computed from `ws_longitude` /
`ws_latitude` with the [Urbanity Python package](https://urbanity.readthedocs.io/en/latest/index.html).
For indicator definitions see [Table 1](https://www.nature.com/articles/s41597-023-02578-1/tables/1)
of Yap, W., Biljecki, F. *A Global Feature-Rich Network Dataset of Cities and Dashboard for
Comprehensive Urban Analyses.* Sci Data 10, 667 (2023),
<https://www.nature.com/articles/s41597-023-02578-1>. Streetscape and POI indicators are
zero-inflated (many locations have none nearby).

**Building morphology**

| Column | Type | Unit | Description |
|---|---|---|---|
| `Footprint Proportion` | float | % | Building footprint proportion |
| `Footprint Mean` | float | m² | Mean footprint area |
| `Footprint Stdev` | float | m² | Footprint area standard deviation |
| `Perimeter Total` | float | m | Total footprint perimeter |
| `Perimeter Mean` | float | m | Mean footprint perimeter |
| `Perimeter Stdev` | float | m | Perimeter standard deviation |
| `Complexity Mean` | float | m | Mean footprint complexity |
| `Complexity Stdev` | float | m | Complexity standard deviation |
| `Building Count` | float | count | Number of buildings |

**Population**

| Column | Type | Unit | Description |
|---|---|---|---|
| `PopSum` | float | count | Total population |
| `Men` | float | count | Male population |
| `Women` | float | count | Female population |
| `Elderly` | float | count | Elderly (aged 60+) population |
| `Youth` | float | count | Young (15–24) population |
| `Children` | float | count | Child (< 5) population |

**Points of interest** (amenity counts)

| Column | Type | Unit | Description |
|---|---|---|---|
| `Civic` | float | count | Civic amenities |
| `Commercial` | float | count | Commercial amenities |
| `Entertainment` | float | count | Entertainment amenities |
| `Food` | float | count | Food amenities |
| `Healthcare` | float | count | Healthcare amenities |
| `Institutional` | float | count | Institutional amenities |
| `Recreational` | float | count | Recreational amenities |
| `Social` | float | count | Social amenities |

**Streetscape view indices** (each provided as `… Mean` and `… Stdev`; dimensionless)

| Column pair | Type | Unit | Description |
|---|---|---|---|
| `Green View Mean` / `Green View Stdev` | float | – | Green view index (mean, st.dev.) |
| `Sky View Mean` / `Sky View Stdev` | float | – | Sky view index (mean, st.dev.) |
| `Building View Mean` / `Building View Stdev` | float | – | Building view index (mean, st.dev.) |
| `Road View Mean` / `Road View Stdev` | float | – | Road view index (mean, st.dev.) |
| `Visual Complexity Mean` / `Visual Complexity Stdev` | float | – | Visual complexity index (mean, st.dev.) |

### G · Pre-survey aggregates & H · Post-survey aggregates (`_after`)

Each wearable-health and weather **stream** is summarized by a set of **statistics** over
three **windows**, twice: once looking **back** from the survey moment (pre-survey, group G)
and once looking **forward** from it (post-survey, group H, `_after` suffix).

**Naming scheme**

- Pre-survey:  `{stream}_{statistic}_{window}` &nbsp;→&nbsp; window is the half-open interval `(start − W, start]`.
- Post-survey: `{stream}_{statistic}_{window}_after` &nbsp;→&nbsp; window is the half-open interval `(start, start + W]`.

where `start = ws_timestamp_start` and `W ∈ {10min, 1h, 6h}`.

**Windows (`W`)**

| Suffix | Span | Use |
|---|---|---|
| `10min` | 10 minutes | Tightest look-around the survey moment. |
| `1h` | 1 hour | Working aggregate used throughout the analysis. |
| `6h` | 6 hours | Widest coverage / longest context. |

**Streams**

| Prefix | Stream | Source |
|---|---|---|
| `hr` | Heart rate | Wearable health |
| `rhr` | Resting heart rate | Wearable health |
| `spo2` | Blood oxygen (SpO₂) | Wearable health |
| `steps` | Step count | Wearable health |
| `walk` | Walking/running distance | Wearable health |
| `stand` | Stand time | Wearable health |
| `audio` | Ambient sound level | Wearable audio |
| `temp` | Air temperature | Nearest station (outdoor ambient) |
| `rh` | Relative humidity | Nearest station (outdoor ambient) |
| `heat_index` | Heat index | Derived from `temp` + `rh` |
| `wind_speed` | Wind speed | Nearest station (outdoor ambient) |
| `wind_dir` | Wind direction | Nearest station (outdoor ambient) |
| `rain` | Rainfall | Nearest station (outdoor ambient) |

> Weather columns are **outdoor ambient** context from the nearest government station — not
> the participant's actual (often indoor / air-conditioned) microclimate.

Weather observations were retrieved from Singapore's National Environment Agency (NEA) via
[data.gov.sg](https://beta.data.gov.sg/collections/1459/view), with each response matched to
its nearest station (`weather_station_id`, `weather_station_dist_km`). Source parameter
units and instrument accuracy:

| Measurement (stream) | Unit | Accuracy |
|---|---|---|
| Air temperature (`temp`) | °C | ±0.1 °C |
| Relative humidity (`rh`) | % | ±1 % |
| Rainfall (`rain`) | mm | 2 % at 1 l/h |
| Wind speed (`wind_speed`) | knots | 0–35 m/s: ±0.3 m/s or ±3 % (whichever is greater); 35–60 m/s: ±5 % |
| Wind direction (`wind_dir`) | ° | ±3° |

Heat index (`heat_index`) is derived from `temp` and `rh` (not a measured stream).

**Statistics**

| Suffix | Meaning |
|---|---|
| `count` | Number of samples in the window. |
| `mean`, `median`, `min`, `max`, `std` | Standard summaries (availability varies by stream). |
| `total` | Accumulated value over the window (movement streams: `steps`, `walk`, `stand`). |
| `max5min` | Peak 5-minute rainfall within the window (`rain` only). |

**Pre-survey-only derived features** (group G, no `_after` counterpart): coverage flags
`has_hr_data`, `has_steps_data`, `has_walk_data`; an activity indicator `high_activity`; and
log-scaled movement totals `log_steps_total`, `log_walk_total`.

Example columns: `hr_mean_1h`, `steps_total_6h`, `audio_max_10min`, `temp_mean_1h`,
`heat_index_mean_1h`, `rain_total_1h` (pre-survey) and their `_after` counterparts
`hr_mean_1h_after`, `temp_mean_1h_after`, `heat_index_mean_1h_after` (post-survey).

## Notes on the two most recent additions

- **`ws_timestamp_submit`** records when each response was submitted, enabling a survey
  completion duration (`ws_timestamp_submit − ws_timestamp_start`). It is stored as a
  timezone-aware UTC timestamp to match `ws_timestamp_start`.
- **Post-survey `_after` aggregates** mirror the pre-survey wearable-health and weather
  summaries over look-ahead windows `(start, start + W]`, supporting before/after comparisons
  around the survey moment. They are additive; all previously released columns are unchanged.

## Privacy protection applied to this release

To reduce the risk of identifying participants from their home location, exact home
coordinates are **not** released. For every response reported at home
(`q_location == 'Indoor - Home'`), the recorded longitude/latitude were spatially
generalized: the coordinates were converted to a hexagonal grid with an edge length of
approximately 200 m and then converted back to longitude/latitude. As a result, all home
responses that fall within the same ~200 m cell share a single, coarsened coordinate.

- The transformation is **lossy and non-invertible**: the original home point cannot be
  recovered from the released coordinate.
- Coordinates for all **non-home** responses and **all non-coordinate fields** are
  unchanged from the source data.
- The exact-coordinate data are retained only in a **private** repository that is never
  released publicly.

**Coordinates and Figures 4-15.** None of Figures 4-15 use participant coordinates, so
the privacy protection does not affect any figure reproduced in this repository; the
regenerated figures are identical to the manuscript versions. (Figure 3, the spatial
response maps, does require exact coordinates and therefore cannot be reproduced from this
public dataset.)

## Provenance

This dataset is a privacy-protected derivative of an internal, QC-gated aggregation
pipeline. The internal pipeline, exact-coordinate data, and full analysis notebooks are
maintained in a separate private repository and are not part of this public release.
