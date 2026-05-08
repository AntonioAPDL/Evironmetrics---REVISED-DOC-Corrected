# Article Asset Review Report

This report groups the current revised-article figures and tables by provenance role so they can be reviewed visually and operationally.

Manifest contract: `ARTICLE_GENERATED_ASSET_MANIFEST.json`

Primary visual gallery: `generated/article_asset_review/figure_gallery.html`

Primary wiring audit: `generated/article_asset_review/CURRENT_MODEL_OUTPUT_WIRING_AUDIT.md`

## Review priorities

1. Check that setup/input figures are legible and still appropriate.
2. Check that `fig:synth1` matches the intended representative selected-model story.
3. Check that historical-summary figures read as descriptive support rather than validation evidence.
4. Check that appendix support figures/tables are still placed appropriately.

## Setup / Inputs

| Label | Role | Article file | Generated source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:sanlorenzo` | Study-setting figure | `usgs.png` | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/usgs.png` | 241 | yes | Representative 2022-12-25 setup/support v2 figure |
| `fig:covariates` | Covariate setup figure | `precip_soilmoisture_climatePC1_faceted_labeled.png` | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/precip_soilmoisture_climatePC1_faceted_labeled.png` | 262 | yes | Representative 2022-12-25 setup/support v2 figure |
| `fig:retrospectives` | Retrospective-product setup figure | `retrospective_log_discharge_plot_faceted.png` | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/retrospective_log_discharge_plot_faceted.png` | 277 | yes | Representative 2022-12-25 setup/support v2 figure |
| `fig:ensembles` | Forecast-product setup figure | `forecats.png` | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/forecats.png` | 328 | yes | Representative 2022-12-25 setup/support v2 figure |

## Historical Summaries

| Label | Role | Article file | Generated source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:dry_quantile` | Dry-period historical summary | `All_exal_2012-2016_DISC.png` | `generated/current_model_output_support/figures/All_exal_2012-2016_DISC.png` | 368 | yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:rainy_quantile` | Rainy-period historical summary | `All_exal_2017-2019_DISC.png` | `generated/current_model_output_support/figures/All_exal_2017-2019_DISC.png` | 377 | yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:80_components` | Long-cycle component summary | `80_component_1991_2022.png` | `generated/current_model_output_support/figures/80_component_1991_2022.png` | 460 | yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |

## Selected Model

| Label | Role | Article file | Generated source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:synth1` | Representative selected-model synthesis | `posterior_samples_valid.png` | `generated/exal_m_t1_20221225/posterior_samples_valid.png` | 395 | yes | Verified representative 2022-12-25 exAL-M-T1 output |

## Appendix Support

| Label | Role | Article file | Generated source | TeX line | Wired to current outputs? | Note |
|---|---|---|---|---:|---|---|
| `fig:synth2` | Historical-only reference synthesis | `posterior_samples_counter_valid.png` | `generated/current_model_output_support/figures/posterior_samples_counter_valid.png` | 474 | yes | Copied from the current 2022-12-25 exdqlm_univar publication-style output bundle |

## Tables

| Label | Role | Generated include | TeX line | Note |
|---|---|---|---:|---|
| `tab:benchmark_crps_models` | Five-cutoff benchmark table | `generated/article_table_includes/table_benchmark_crps_rows.tex` | 343 | Generated from the frozen HE2 publication manifest plus the raw-baseline rows in the five exAL-M-T1 CRPS summaries |
| `tab:components_23_31` | Representative covariate-effects table | `generated/article_table_includes/table_components_23_31_rows.tex` | 358 | Generated from the representative 2022-12-25 exAL-M-T1 covariate-effects export |
| `tab:gamma_sigma_intervals1` | Appendix gamma summary | `generated/article_table_includes/table_gamma_rows.tex` | 453 | Generated from the representative 2022-12-25 exAL-M-T1 gamma export |
| `tab:gamma_sigma_intervals2` | Appendix sigma summary | `generated/article_table_includes/table_sigma_rows.tex` | 453 | Generated from the representative 2022-12-25 exAL-M-T1 sigma export |

## Generated manifests

- `generated/article_asset_review/figure_manifest.csv`
- `generated/article_asset_review/table_manifest.csv`
- `generated/article_asset_review/CURRENT_MODEL_OUTPUT_WIRING_AUDIT.md`
