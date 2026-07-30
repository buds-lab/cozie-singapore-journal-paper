# Journal figure assets

This folder contains rendered figure assets used by `../main.tex`. It contains no raw survey records or participant-level source data.

## Folder structure

- `methods/` — study-design and micro-survey visuals copied from `orenth-usk-data-INTERNAL/2_visualizations/`.
- `data_characterization/` — rendered figures generated from `orenth-usk-data-INTERNAL/5_analysis_spaces/notebooks/01_Data_Characterization.ipynb`.

## Source and reproducibility map

| Journal asset | Source asset or notebook figure |
|---|---|
| `methods/cozie_study_design.pdf` | `2_visualizations/Usk_Orenth Cozie Diagram.pdf` |
| `methods/cozie_microsurvey.pdf` | `2_visualizations/Orenth-Usk_high_quality.pdf` |
| `data_characterization/survey_response_flow.pdf` | `01_Data_Characterization.ipynb`, Figure C1 |
| `data_characterization/survey_battery_and_coverage.pdf` | `01_Data_Characterization.ipynb`, Figure A1 |
| `data_characterization/wearable_health_windows.pdf` | `01_Data_Characterization.ipynb`, Figure A2 |
| `data_characterization/outdoor_weather_windows.pdf` | `01_Data_Characterization.ipynb`, Figure A3 |
| `data_characterization/response_density_and_grid_counts.png` | `01_Data_Characterization.ipynb`, Figure B4 |
| `data_characterization/weekly_temporal_cadence.pdf` | `01_Data_Characterization.ipynb`, Figure D2 |
| `data_characterization/space_type_timing_heatmaps.pdf` | `01_Data_Characterization.ipynb`, Figure D4 |
| `data_characterization/participant_engagement.pdf` | `01_Data_Characterization.ipynb`, Figure E2 |
| `data_characterization/cooling_preference.pdf` | `01_Data_Characterization.ipynb`, Figure F2 |
| `data_characterization/noise_characterization.pdf` | `01_Data_Characterization.ipynb`, Figure G1 |

## Regeneration

The notebook contains explicit `fig.savefig(...)` / `fig_density.write_image(...)` commands for each notebook-derived asset. Execute its setup cell and the relevant labelled figure cells to regenerate the PDFs in `5_analysis_spaces/figures/`, then copy the rendered files here using the mapping above.

`main.tex` intentionally retains placeholder captions. Captions, interpretation, and manuscript prose are to be supplied and approved by the authors.
