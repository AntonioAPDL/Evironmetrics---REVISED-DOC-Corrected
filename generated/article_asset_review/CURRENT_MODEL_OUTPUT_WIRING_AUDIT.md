# Current Model-Output Wiring Audit

This audit is generated from `ARTICLE_GENERATED_ASSET_MANIFEST.json` and the current article-side generated bundles.

## Figure and Table Status

| Manuscript object | Current article number | Current source | Current-model-output wired? | Notes |
|---|---|---|---:|---|
| `fig:sanlorenzo` | Figure 1 | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/usgs.png` -> `DISC/usgs.png` | Yes | Representative 2022-12-25 setup/support v2 figure |
| `fig:covariates` | Figure 2 | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/precip_soilmoisture_climatePC1_faceted_labeled.png` -> `DISC/precip_soilmoisture_climatePC1_faceted_labeled.png` | Yes | Representative 2022-12-25 setup/support v2 figure |
| `fig:retrospectives` | Figure 3 | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/retrospective_log_discharge_plot_faceted.png` -> `DISC/retrospective_log_discharge_plot_faceted.png` | Yes | Representative 2022-12-25 setup/support v2 figure |
| `fig:ensembles` | Figure 4 | `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/forecats.png` -> `DISC/forecats.png` | Yes | Representative 2022-12-25 setup/support v2 figure |
| `fig:dry_quantile` | Figure 5 | `generated/current_model_output_support/figures/All_exal_2012-2016_DISC.png` -> `DISC/All_exal_2012-2016_DISC.png` | Yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:rainy_quantile` | Figure 6 | `generated/current_model_output_support/figures/All_exal_2017-2019_DISC.png` -> `DISC/All_exal_2017-2019_DISC.png` | Yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:synth1` | Figure 7 | `generated/exal_m_t1_20221225/posterior_samples_valid.png` -> `DISC/posterior_samples_valid.png` | Yes | Verified representative 2022-12-25 exAL-M-T1 output |
| `fig:80_components` | Figure A1 | `generated/current_model_output_support/figures/80_component_1991_2022.png` -> `DISC/80_component_1991_2022.png` | Yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:synth2` | Figure A2 | `generated/current_model_output_support/figures/posterior_samples_counter_valid.png` -> `DISC/posterior_samples_counter_valid.png` | Yes | Copied from the current 2022-12-25 exdqlm_univar publication-style output bundle |
| `tab:benchmark_crps_models` | Table 1 | `generated/article_table_includes/table_benchmark_crps_rows.tex` | Yes | Generated from the frozen HE2 publication manifest plus the raw-baseline rows in the five exAL-M-T1 CRPS summaries; now auto-included into TeX |
| `tab:components_23_31` | Table 2 | `generated/article_table_includes/table_components_23_31_rows.tex` | Yes | Generated from the representative 2022-12-25 exAL-M-T1 covariate-effects export; now auto-included into TeX |
| `tab:gamma_sigma_intervals1` | Table A.1 | `generated/article_table_includes/table_gamma_rows.tex` | Yes | Generated from the representative 2022-12-25 exAL-M-T1 gamma export; now auto-included into TeX |
| `tab:gamma_sigma_intervals2` | Table A.2 | `generated/article_table_includes/table_sigma_rows.tex` | Yes | Generated from the representative 2022-12-25 exAL-M-T1 sigma export; now auto-included into TeX |
