# Current Model-Output Wiring Audit

This audit is generated from `MANUSCRIPT_ASSET_MANIFEST.json` and the current article-side artifact bundles.

## Figure and Table Status

| Manuscript object | Current article number | Manuscript path | Artifact source | Current-model-output wired? | Notes |
|---|---|---|---|---:|---|
| `fig:sanlorenzo` | Figure 1 | `figures/manuscript/site_context_usgs.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/usgs.png` | Yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |
| `fig:covariates` | Figure 2 | `figures/manuscript/covariate_context_precip_soil_gdpc.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/precip_soilmoisture_climatePC1_faceted_labeled.png` | Yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |
| `fig:retrospectives` | Figure 3 | `figures/manuscript/retrospective_products_context.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/retrospective_log_discharge_plot_faceted.png` | Yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |
| `fig:ensembles` | Figure 4 | `figures/manuscript/forecast_products_context.png` | `artifacts/five_cutoff_setup_support/20221225_exal_m_t1/figures/forecats.png` | Yes | Representative 2022-12-25 setup/support figure from the canonical five-cutoff support bundle |
| `fig:dry_quantile` | Figure 5 | `figures/manuscript/historical_summary_dry_period.png` | `artifacts/historical_support_from_current_models/figures/historical_summary_dry_period.png` | Yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:rainy_quantile` | Figure 6 | `figures/manuscript/historical_summary_wet_period.png` | `artifacts/historical_support_from_current_models/figures/historical_summary_wet_period.png` | Yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:synth1` | Figure 7 | `figures/manuscript/representative_synthesis_multivariate.png` | `artifacts/representative_selected_model_2022_12_25/representative_synthesis_multivariate.png` | Yes | Corrected representative 2022-12-25 exAL-M-T1 output from the he2pubgdpc1r1 relaunch |
| `fig:80_components` | Figure A1 | `figures/manuscript/historical_component_80month.png` | `artifacts/historical_support_from_current_models/figures/historical_component_80month.png` | Yes | Rendered from the current 2022-05-11 exAL-M-T1 full-history multivariate run |
| `fig:synth2` | Figure A2 | `figures/manuscript/reference_synthesis_univariate.png` | `artifacts/historical_support_from_current_models/figures/reference_synthesis_univariate.png` | Yes | Copied from the current 2022-12-25 exdqlm_univar publication-style output bundle |
| `tab:benchmark_crps_models` | Table 1 | `tables/generated_tex/benchmark_crps_main_table.tex` | `artifacts/he2_publication_freeze/he2_bayesian_publication_manifest.csv, artifacts/five_cutoff_crps_validation_sources` | Yes | Generated from the frozen HE2 publication manifest plus the raw-baseline rows in the five exAL-M-T1 CRPS summaries; now auto-included into TeX |
| `tab:components_23_31` | Table 2 | `tables/generated_tex/representative_covariate_effects_table.tex` | `artifacts/representative_selected_model_2022_12_25/covariate_effects_summary.csv` | Yes | Generated from the representative 2022-12-25 exAL-M-T1 covariate-effects export; now auto-included into TeX |
| `tab:gamma_sigma_intervals1` | Table A.1 | `tables/generated_tex/appendix_gamma_summary_table.tex` | `artifacts/representative_selected_model_2022_12_25/gamma_summary.csv` | Yes | Generated from the representative 2022-12-25 exAL-M-T1 gamma export; now auto-included into TeX |
| `tab:gamma_sigma_intervals2` | Table A.2 | `tables/generated_tex/appendix_sigma_summary_table.tex` | `artifacts/representative_selected_model_2022_12_25/sigma_summary.csv` | Yes | Generated from the representative 2022-12-25 exAL-M-T1 sigma export; now auto-included into TeX |
