# Article Asset Review Report

This report groups the current revised-article figures and tables by provenance role so they can be reviewed visually and operationally.

Manifest contract: `MANUSCRIPT_ASSET_MANIFEST.json`

Primary visual gallery: `reports/manuscript_asset_review/figure_gallery.html`

Primary wiring audit: `reports/manuscript_asset_review/CURRENT_MODEL_OUTPUT_WIRING_AUDIT.md`

## Review priorities

1. Check that setup/input figures are legible and still appropriate.
2. Check that `fig:synth1` matches the intended representative selected-model story.
3. Check that historical-summary figures read as descriptive support rather than validation evidence.
4. Check that appendix support figures and tables are still placed appropriately.

## Setup / Inputs

| Label | Role | Manuscript path | Artifact source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:sanlorenzo` | Study-setting figure | `figures/manuscript/site_context_usgs.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/usgs.png` | 251 | yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |
| `fig:covariates` | Covariate setup figure | `figures/manuscript/covariate_context_precip_soil_gdpc.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/precip_soilmoisture_climatePC1_faceted_labeled.png` | 272 | yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |
| `fig:retrospectives` | Retrospective-product setup figure | `figures/manuscript/retrospective_products_context.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/retrospective_log_discharge_plot_faceted.png` | 287 | yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |
| `fig:ensembles` | Forecast-product setup figure | `figures/manuscript/forecast_products_context.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/forecats.png` | 338 | yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |

## Historical Summaries

| Label | Role | Manuscript path | Artifact source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:dry_quantile` | Dry-period historical summary | `figures/manuscript/historical_summary_dry_period.png` | `artifacts/historical_support_from_current_models/figures/historical_summary_dry_period.png` | 378 | yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:rainy_quantile` | Rainy-period historical summary | `figures/manuscript/historical_summary_wet_period.png` | `artifacts/historical_support_from_current_models/figures/historical_summary_wet_period.png` | 387 | yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:80_components` | Long-cycle component summary | `figures/manuscript/historical_component_80month.png` | `artifacts/historical_support_from_current_models/figures/historical_component_80month.png` | 470 | yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |

## Selected Model

| Label | Role | Manuscript path | Artifact source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:synth1` | Representative selected-model synthesis | `figures/manuscript/representative_synthesis_multivariate.png` | `artifacts/representative_selected_model_2022_12_25/representative_synthesis_multivariate.png` | 405 | yes | Corrected representative 2022-12-25 exAL-M-T1 output from the he2pubgdpc1r1 relaunch |

## Appendix Support

| Label | Role | Manuscript path | Artifact source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:synth2` | Historical-only reference synthesis | `figures/manuscript/reference_synthesis_univariate.png` | `artifacts/historical_support_from_current_models/figures/reference_synthesis_univariate.png` | 484 | yes | Copied from the current 2022-12-25 exdqlm_univar publication-style output bundle |

## Tables

| Label | Role | Generated include | TeX line | Note |
|---|---|---|---:|---|
| `tab:benchmark_crps_models` | Five-cutoff benchmark table | `tables/generated_tex/benchmark_crps_main_table.tex` | 355 | Generated from the frozen HE2 publication manifest plus the raw-baseline rows in the five exAL-M-T1 CRPS summaries |
| `tab:components_23_31` | Representative covariate-effects table | `tables/generated_tex/representative_covariate_effects_table.tex` | 366 | Generated from the representative 2022-12-25 exAL-M-T1 covariate-effects export |
| `tab:gamma_sigma_intervals1` | Appendix gamma summary | `tables/generated_tex/appendix_gamma_summary_table.tex` | 459 | Generated from the representative 2022-12-25 exAL-M-T1 gamma export |
| `tab:gamma_sigma_intervals2` | Appendix sigma summary | `tables/generated_tex/appendix_sigma_summary_table.tex` | 461 | Generated from the representative 2022-12-25 exAL-M-T1 sigma export |

## Generated manifests

- `reports/manuscript_asset_review/figure_manifest.csv`
- `reports/manuscript_asset_review/table_manifest.csv`
- `reports/manuscript_asset_review/CURRENT_MODEL_OUTPUT_WIRING_AUDIT.md`
