# Figure and Table Provenance Inventory

## Scope

This document records the current provenance status of manuscript figures and interpretation-dependent tables for the revised Environmetrics article.

Primary manuscript repo:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/Evironmetrics---REVISED-DOC-2`

Primary workflow repo currently linked to figure/table generation:
- `/data/muscat_data/jaguir26/project1_ucsc_phd`

Main purpose:
- identify which manuscript outputs are already traceable to the current workflow,
- distinguish reproducible workflow-linked outputs from legacy or ambiguous outputs,
- and define the next regeneration tasks needed to align all interpretation material with the final selected `exAL-M-T1` analysis behind Table 1.

Companion relaunch document:
- `EXAL_M_T1_RELAUNCH_CHECKLIST.md`
  - This records the exact cutoff-by-cutoff source runs behind the published `exAL-M-T1` CRPS values, the required rerun artifacts, and the post-rerun validation contract.

Setup/support figure correction plan:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/EXAL_M_T1_SETUP_SUPPORT_V2_SOURCE_MANIFEST.md`
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/EXAL_M_T1_SETUP_SUPPORT_V2_FILE_PLAN.md`
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/EXAL_M_T1_SETUP_SUPPORT_V2_ACCEPTANCE_CHECKLIST.md`

Canonical forward runbook:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/CANONICAL_REVISED_ARTICLE_WORKFLOW.md`
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/HE2_FULL_HISTORY_REPAIR_FORWARD_PLAN.md`

Article-side provenance refresh helper:
- `ARTICLE_GENERATED_ASSET_MANIFEST.json`
- `scripts/refresh_local_provenance_bundles.py`
- `scripts/refresh_exal_m_t1_generated_assets.py`
- `scripts/refresh_he2_manifest_snapshot.py`
- `scripts/build_generated_table_includes.py`
- `scripts/promote_generated_figures_to_disc.py`
- `scripts/build_setup_support_by_cutoff_v2_appendix.py`
- `scripts/build_generated_asset_index.py`
- `scripts/refresh_all_generated_assets.py`

Article-side review outputs:
- `generated/article_asset_review/ARTICLE_ASSET_REVIEW.md`
- `generated/article_asset_review/figure_gallery.html`
- `generated/article_asset_review/CURRENT_MODEL_OUTPUT_WIRING_AUDIT.md`
- `generated/article_asset_selection/selection_manifest.json`
- `generated/article_table_includes/README.md`
- `generated/README.md`
- `generated/asset_inventory.csv`
- `generated/he2_historical_support_audit_20260507/historical_support_audit.md`
- `generated/setup_support_by_cutoff_v2_appendix/README.md`

This inventory now distinguishes three reproducibility levels:
- objects frozen locally in the article repo and tied to verified selected-model reruns,
- objects frozen locally in the article repo as workflow-linked support figures,
- and the underlying workflow-side generators that remain the authoritative reproduction path.

## Overall conclusion

The manuscript repo is **not fully self-contained** for figure/table generation. It now contains frozen local provenance bundles for all current figure/table assets used by the article, but the authoritative generators still live in the workflow repo above.

Most important results from this audit:
- every figure file currently used by the manuscript and checked below matches the workflow repo's recorded gold hash exactly.
- every current figure/table asset in the article is now either:
  - tied to a verified selected-model rerun bundle,
  - or frozen locally as a workflow-linked support figure.
- the manuscript-facing `DISC/` figures are now promoted from a source-controlled generated-asset manifest rather than by manual selection.
- the model-derived manuscript tables now consume generated `\\input{}` row includes rebuilt from frozen article-side CSV sources.

That means the current manuscript figures are strongly linked to the current workflow repo, even though the manuscript repo itself does not carry the full generation scripts.

The clean current generator contract is:
- `R/unified/stages/stage_post.R`
- `scripts/run_environmetrics_figures.R`
- `R/environmetrics/40_figures.R`

The article-side generated asset freeze point is now indexed under:
- `generated/README.md`
- `generated/asset_inventory.csv`

The appendix-ready composite cutoff panels now live under:
- `generated/setup_support_by_cutoff_v2_appendix/`

The weaker historical entrypoint is:
- `scripts/make_environmetrics_figures.R`

That legacy script still relies on notebook-linearized state and hard-coded external paths, so it should not be treated as the primary current reproduction contract.

## 2026-05-06 selected-model refresh status

The representative selected-model refresh is now partially complete.

Verified source run:
- `/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_publication_replay_representatives_20260506/20221225_exal_m_t1/runs/multimodel_20221225_v8_exalm_t1_discount_grid_exact_v1_set09_exdqlm_multivar_keep`

Verified status:
- `validation_status=pass`
- `compare_status=pass`
- deterministic-climate validation passes
- posterior table exports are present

The revised manuscript repo now contains a local copy of the representative selected-model artifacts under:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/Evironmetrics---REVISED-DOC-2/generated/exal_m_t1_20221225`

Those copied artifacts include:
- `posterior_samples_valid.png`
- `covariate_effects_summary.csv/.tex`
- `gamma_summary.csv/.tex`
- `sigma_summary.csv/.tex`
- `posterior_table_exports_manifest.csv`

Current manuscript refreshes already tied to that verified run:
- `DISC/posterior_samples_valid.png`
- `tab:components_23_31`
- `tab:gamma_sigma_intervals1`
- `tab:gamma_sigma_intervals2`

The narrow exAL-M-T1 relaunch is now verified across all five publication cutoffs.

The exact manuscript-side artifact mapping is recorded in:
- `EXAL_M_T1_ARTIFACT_RUN_MAP.md`

That companion file should now be treated as the most direct answer to:
- which manuscript objects are locked to the verified five-run keep lineage,
- which objects are already refreshed from the representative `2022-12-25` run,
- and which remaining figures are workflow-linked support objects outside the narrow keep-run source set.

The revised manuscript repo now also contains two article-side frozen support bundles:
- `generated/historical_summary_sources/`
- `generated/workflow_linked_support_sources/`

It now also contains a dedicated cutoff-specific setup/support figure family derived from the five verified `exAL-M-T1` run bundles:
- `generated/setup_support_by_cutoff_v2/`
- `generated/setup_support_by_cutoff_v2_review/`

That family is produced from the current workflow-side derivation path:
- `config/exal_m_t1_setup_support_by_cutoff_v2_20260507.json`
- `scripts/render_exal_m_t1_setup_support_by_cutoff_v2.py`
- `scripts/render_setup_support_bundle_v2.R`
- `scripts/setup_support_bundle_v2_helpers.R`
- `scripts/validate_exal_m_t1_setup_support_v2.py`
- `repro/run/EXAL_M_T1_SETUP_SUPPORT_BY_CUTOFF_V2_WORKFLOW.md`

Current article-facing status:
- the corrected `v2` setup/support family is now implemented, validated, and mirrored locally;
- the manuscript-facing `DISC/` copies are promoted from the representative `20221225_exal_m_t1` bundle;
- the older `20260506` setup/support family remains archived only as a provisional `v1` audit artifact.

Both support bundles can now be refreshed through:
- `scripts/refresh_local_provenance_bundles.py`

The representative selected-model bundle and the HE2 snapshot can now be refreshed through:
- `scripts/refresh_exal_m_t1_generated_assets.py`
- `scripts/refresh_he2_manifest_snapshot.py`

The preferred top-level article-side refresh entrypoint is:
- `scripts/refresh_all_generated_assets.py`

## Current workflow evidence

### Figure-generation evidence

The workflow repo contains the following direct figure-generation references:
- authoritative current path:
  - `R/environmetrics/40_figures.R`
  - `scripts/run_environmetrics_figures.R`
  - `R/unified/stages/stage_post.R`
- legacy / historical references:
  - `scripts/make_environmetrics_figures.R`
  - `Environmetrics_Figures.ipynb`
  - `repro/extracted/Environmetrics_Figures__RECOVERED_WORKING.r`
- provenance / validation:
  - `repro/REPO_MAP.md`
  - `repro/REPRODUCE_PAPER.md`
  - `repro/gold_DISC_figures.sha256`

### Posterior-table export evidence

The workflow repo contains the following table-export infrastructure:
- `R/environmetrics/02_helpers_core.R`
- `R/unified/stages/stage_post.R`
- `R/unified/post_artifact_contract.R`
- `repro/UNIFIED_WORKFLOW_README.md`
- `tests/testthat/test_post_posterior_table_exports.R`

The documented post-stage outputs are:
- `gamma_summary.csv`
- `sigma_summary.csv`
- `covariate_effects_summary.csv`
- optional `.tex` snippets for the same summaries
- `posterior_table_exports_README.md`
- `posterior_table_exports_manifest.csv`

## Figure provenance map

### High-confidence, workflow-linked figures already matching the recorded gold outputs

The following manuscript figure assets in `Evironmetrics---REVISED-DOC-2/DISC/` were hashed locally and match the workflow repo's `repro/gold_DISC_figures.sha256` exactly.

| Manuscript label | Current asset | Current manuscript role | Workflow evidence | Hash match | Repro status | Selected-run status | Recommended action |
|---|---|---|---|---|---|---|---|
| `fig:sanlorenzo` | `DISC/usgs.png` | study-setting figure | corrected cutoff-specific `v2` bundle built from the CRPS-linked `exAL-M-T1` source manifest and authoritative figure-input bundles; manuscript-facing copy promoted from `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/usgs.png`; current contract uses full `1987-05-29 -> cutoff` USGS history | yes | reproducible through validated `v2` workflow and frozen locally | representative `2022-12-25` support role; all five cutoff variants preserved | keep as representative setup/support figure with explicit cutoff-specific provenance |
| `fig:covariates` | `DISC/precip_soilmoisture_climatePC1_faceted_labeled.png` | covariate setup figure | corrected `v2` bundle reads raw cutoff-specific `cov_01_PPT.csv`, `cov_02_SOIL.csv`, and `cov_03_PCA.csv`; manuscript-facing copy promoted from `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/...`; current contract uses full `1987-05-29 -> cutoff` raw covariate history | yes | reproducible through validated `v2` workflow and frozen locally | representative `2022-12-25` support role; all five cutoff variants preserved | keep as representative setup/support figure with explicit cutoff-specific provenance |
| `fig:retrospectives` | `DISC/retrospective_log_discharge_plot_faceted.png` | retrospective-product setup figure | corrected `v2` bundle reads authoritative retrospective lineage / bundle-native retrospective sources; manuscript-facing copy promoted from `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/...`; current contract uses the retrospective support actually available for the selected cutoff and records whether full history is present | yes | reproducible through validated `v2` workflow and frozen locally | representative `2022-12-25` support role; all five cutoff variants preserved | keep as representative setup/support figure with explicit cutoff-specific provenance |
| `fig:ensembles` | `DISC/forecats.png` | forecast-product setup figure | corrected `v2` bundle stages bundle-native forecast inputs through `forecats_plot_bundle.R`; manuscript-facing copy promoted from `generated/setup_support_by_cutoff_v2/20221225_exal_m_t1/figures/...`; current contract uses a strict `cutoff - 28 days` to `cutoff + 28 days` display window | yes | reproducible through validated `v2` workflow and frozen locally | representative `2022-12-25` support role; all five cutoff variants preserved | keep as representative setup/support figure with explicit cutoff-specific provenance |
| `fig:dry_quantile` | `DISC/All_exal_2012-2016_DISC.png` | historical regime illustration | current `2022-05-11 exAL-M-T1` full-history multivariate run rendered through `scripts/render_current_model_output_support_figures.R` and frozen locally in `generated/current_model_output_support/` | yes | reproducible from current model outputs and frozen locally in the article repo | current-model historical-support figure outside the narrow five-run keep lineage | keep with explicit current-output support provenance |
| `fig:rainy_quantile` | `DISC/All_exal_2017-2019_DISC.png` | historical regime illustration | same as above; frozen locally in `generated/current_model_output_support/` | yes | reproducible from current model outputs and frozen locally in the article repo | current-model historical-support figure outside the narrow five-run keep lineage | keep with explicit current-output support provenance |
| `fig:synth1` | `DISC/posterior_samples_valid.png` | predictive synthesis illustration | verified representative rerun bundle in `generated/exal_m_t1_20221225/` plus workflow-side replay validation | yes | reproducible from verified `2022-12-25 exAL-M-T1` rerun bundle and frozen locally | locked to representative `2022-12-25` selected-model run | keep synced to representative selected-model bundle |
| `fig:80_components` | `DISC/80_component_1991_2022.png` | appendix long-cycle seasonal illustration | current `2022-05-11 exAL-M-T1` full-history multivariate run rendered through `scripts/render_current_model_output_support_figures.R` and frozen locally in `generated/current_model_output_support/` | yes | reproducible from current model outputs and frozen locally in the article repo | current-model historical-support figure outside the narrow five-run keep lineage | keep with explicit current-output support provenance |
| `fig:synth2` | `DISC/posterior_samples_counter_valid.png` | appendix historical-only predictive synthesis | current `2022-12-25 exdqlm_univar` publication-style output bundle copied into `generated/current_model_output_support/` | yes | reproducible from current model outputs and frozen locally in the article repo | current-model appendix support figure outside the narrow five-run keep lineage | keep with explicit current-output support provenance |

### Notes on figure confidence

1. The four setup/support figures are now reproduced through the corrected cutoff-specific `v2` workflow.
   - Workflow-side review:
     - `/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/exal_m_t1_setup_support_by_cutoff_v2_20260507/review/`
   - Article-side mirror and review:
     - `generated/setup_support_by_cutoff_v2/`
     - `generated/setup_support_by_cutoff_v2_review/`
   - Representative manuscript promotion:
     - `generated/setup_support_by_cutoff_v2_article_selection/selection_manifest.json`
   - This validated family covers:
     - `usgs.png`
     - `precip_soilmoisture_climatePC1_faceted_labeled.png`
     - `retrospective_log_discharge_plot_faceted.png`
     - `forecats.png`
   - The corrected `v2` contract is now:
     - `usgs.png` and the raw covariate figure use the full `1987-05-29 -> cutoff` daily history available in the selected-run shared inputs
     - `forecats.png` uses a strict `cutoff - 28 days` to `cutoff + 28 days` display window
     - the retrospective figure uses the actual retrospective support available for that cutoff and no longer implies full-history coverage when the selected bundle is short-window
   - The full per-cutoff availability audit is recorded in:
     - `generated/setup_support_by_cutoff_v2_review/SETUP_SUPPORT_BY_CUTOFF_V2_REVIEW.md`
   - The older `20260506` `v1` family remains archived only as an audit/debugging artifact.

2. `forecats.png` remains more delicate than the other setup figures, but the canonical `v2` path now stages bundle-native forecast inputs explicitly.
   - The workflow repo includes a dedicated reproducibility plan at:
     - `repro/FORECATS_INPUTS_AND_WEIGHTING_PLAN.md`
   - The corrected cutoff-specific derivation anchors that figure to the CRPS-linked `exAL-M-T1` source manifest and the authoritative forecats/histfix bundles instead of the older generic paper-level copy.

3. The dry/wet regime figures and the appendix long-cycle figure are now regenerated from current model outputs.
   - They are still outside the narrow five-run `exAL-M-T1` keep-run lineage used for the main benchmark table.
   - They are frozen locally in:
     - `generated/current_model_output_support/`
   - Their role remains descriptive support:
     - current-model historical summaries of the fitted specification,
     - not representative-cutoff outputs,
     - and not a second forecast-validation exercise.

4. The older notebook/manual reproduction notes are now secondary.
   - `repro/REPRODUCE_PAPER.md` and `repro/REPO_MAP.md` remain useful provenance references.
   - But the clean current reproduction path is the run-scoped unified workflow:
     - `stage_post.R` injects the actual shared input paths,
     - `run_environmetrics_figures.R` runs headlessly,
     - `40_figures.R` generates the figures.

5. `fig:synth1` remains the representative selected-model synthesis figure tied to the `2022-12-25` rerun bundle.
   - `fig:synth2` is now refreshed from a current `exdqlm_univar` output bundle.
   - It remains outside the narrow five-run keep-lineage freeze used for the main benchmark table.

## Table provenance map

### Interpretation-dependent tables in the manuscript

| Manuscript label | Current manuscript role | Current provenance evidence | Confidence | Repro status | Selected-run status | Recommended action |
|---|---|---|---|---|---|---|
| `tab:benchmark_crps_models` | main five-cutoff forecast-validation table | HE2 publication manifest plus synchronized manuscript table values; local article-side snapshot in `generated/he2_publication_manifest_snapshot/` | high | validated against the frozen HE2 publication source | main reference table | keep synced to HE2 publication manifest snapshot |
| `tab:components_23_31` | main-text covariate-effects summary | verified representative rerun export frozen locally in `generated/exal_m_t1_20221225/covariate_effects_summary.csv`; workflow export contract and tests remain in repo | high | reproducible from verified `2022-12-25 exAL-M-T1` rerun bundle and frozen locally | locked to representative `2022-12-25` selected-model run | keep synced to representative selected-model bundle |
| `tab:gamma_sigma_intervals1` | supplementary appendix `gamma` summary | verified representative rerun export frozen locally in `generated/exal_m_t1_20221225/gamma_summary.csv`; workflow export contract and tests remain in repo | high | reproducible from verified `2022-12-25 exAL-M-T1` rerun bundle and frozen locally | locked to representative `2022-12-25` support role | keep as supplementary appendix support |
| `tab:gamma_sigma_intervals2` | supplementary appendix `sigma` summary | verified representative rerun export frozen locally in `generated/exal_m_t1_20221225/sigma_summary.csv`; workflow export contract and tests remain in repo | high | reproducible from verified `2022-12-25 exAL-M-T1` rerun bundle and frozen locally | locked to representative `2022-12-25` support role | keep as supplementary appendix support |

### Notes on table confidence

1. Table exports are better documented than they first appeared.
   - The workflow repo has a formal post-stage artifact contract.
   - Export helpers and tests are already in place.
   - The missing piece is the exact run-level linkage for the current manuscript tables.

2. `tab:components_23_31` is now locked to the representative `2022-12-25` selected-model rerun.
   - The manuscript and local provenance bundle now use the verified `covariate_effects_summary.csv` export from that run.

3. The appendix `gamma` and `sigma` tables are now explicitly treated as supplementary representative-cutoff support.
   - They are frozen locally from the same verified `2022-12-25` rerun bundle.
   - They are no longer described as central forecast-validation evidence.

## Provenance classification for the next phase

### Group A: keep as cutoff-specific setup/support figures
These are now reproduced through the corrected `v2` per-cutoff family derived from the verified five-run `exAL-M-T1` bundles and the authoritative forecats/histfix bundle roots.
- `fig:sanlorenzo`
- `fig:covariates`
- `fig:retrospectives`
- `fig:ensembles`

### Group B: keep as current-model appendix support
- `fig:synth2`

### Group C: selected-run dependent and must be refreshed or verified first
These are too tightly tied to one fitted output to leave ambiguous.
- `fig:synth1`
- `tab:components_23_31`

### Group D: reproducible current-model historical-support figures
These objects are intentionally kept as current-model historical summaries of the fitted specification, rather than as representative-cutoff outputs.
- `fig:dry_quantile`
- `fig:rainy_quantile`
- `fig:80_components`
- `tab:gamma_sigma_intervals1`
- `tab:gamma_sigma_intervals2`

## Locked provenance policy

The following policy is now adopted for the revised manuscript and should govern the regeneration work that follows.

### Section 4: forecast-validation evidence
- Section 4 remains the manuscript's five-cutoff forecast-validation evidence.
- Its benchmark values must continue to come from the validated five-cutoff `exdqlm_multivar_keep` / `exAL-M-T1` comparison workflow.
- Any rerun used to refresh those values must preserve the same configuration that produced the published CRPS table.

### Section 5: representative selected-model interpretation
- Section 5 will use one representative final cutoff of the selected specification.
- The representative cutoff is fixed as `2022-12-25`, because:
  - it is already the manuscript's current illustrative forecast origin,
  - a recent validated workflow run exists for it, and
  - that run already produces publication-facing cutoff-window synthesis artifacts.
- Therefore, the following Section 5 objects must be regenerated or re-verified from the `2022-12-25` `exdqlm_multivar_keep` run:
  - `fig:synth1`
  - `tab:components_23_31`

### Appendix: historical summaries of the selected specification
- Appendix figures and tables remain historical summaries of the selected specification rather than representative-cutoff illustrations.
- This applies to:
  - `fig:dry_quantile`
  - `fig:rainy_quantile`
  - `fig:80_components`
  - `tab:gamma_sigma_intervals1`
  - `tab:gamma_sigma_intervals2`
- The captions and nearby text should continue to say so clearly.
- For the three historical-summary figures, the revised article repo now includes a locked local provenance bundle at:
  - `generated/historical_summary_sources/`
- That bundle preserves:
  - article-side copies of the exact PNGs,
  - SHA-256 hashes matching the workflow gold manifests,
  - and source references to the workflow script and reproduction docs.

## Recent selected-model workflow status

A recent validated family of selected-model runs exists under:
- `/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_quantile_featurecov_ndlm_discount_probe_20260422/runs/`

For all five manuscript cutoffs, the corresponding `exdqlm_multivar_keep` runs:
- passed validation,
- passed deterministic-climate checks,
- use forecast precipitation after the cutoff,
- use forecast soil moisture after the cutoff,
- and keep the PCA/GDPC covariate in passthrough mode rather than forecasting it the same way.

These runs already provide:
- cutoff-window posterior-synthesis figures,
- cutoff-window quantile CSV exports,
- CRPS summary tables,
- and run-scoped manifests and input hashes.

Resolved gaps from this audit:
- the narrow `exAL-M-T1` replay path was completed with the required post-export fixes, so the representative selected-model outputs and posterior interpretation tables are now frozen locally in the revised article repo.
- the cutoff-dependent setup/support figures are now mirrored locally in the revised article repo through:
  - `generated/setup_support_by_cutoff_v2/`
  - `generated/setup_support_by_cutoff_v2_review/`
- the manuscript-facing `DISC/` copies for `fig:sanlorenzo`, `fig:covariates`, `fig:retrospectives`, and `fig:ensembles` are now promoted from the representative `20221225_exal_m_t1` `v2` bundle through:
  - `generated/setup_support_by_cutoff_v2_article_selection/selection_manifest.json`
- the appendix historical-only reference synthesis remains frozen locally through:
  - `generated/workflow_linked_support_sources/`
- In practice, this means:
  - `fig:synth1`, `tab:components_23_31`, `tab:gamma_sigma_intervals1`, and `tab:gamma_sigma_intervals2` are now locked to verified article-side bundles, and
  - the historical-summary figures are preserved separately through the local provenance bundle under `generated/historical_summary_sources/`,
  - while `fig:synth2` is preserved through `generated/workflow_linked_support_sources/`, and the four setup/support figures are now preserved through the validated `v2` cutoff family, with the older `generated/setup_support_by_cutoff/` family retained only as an archival `v1` audit artifact.

## Exact relaunch handoff

The high-level provenance inventory in this file is now paired with a run-level relaunch checklist:
- `EXAL_M_T1_RELAUNCH_CHECKLIST.md`

Use that companion file when:
- identifying the authoritative source run for a given cutoff,
- rerunning the selected specification associated with a published Table 1 CRPS value,
- verifying that the rerun reproduces the selected `exAL-M-T1` CRPS exactly,
- and checking whether the required figure and table artifacts were emitted.

## Current locked state

1. Section 4 remains the five-cutoff validation evidence.
   - `tab:benchmark_crps_models` is now synced to the frozen HE2 publication manifest.

2. Section 5 uses outputs from one representative final cutoff of the selected `exAL-M-T1` specification.
   - `fig:synth1`
   - `tab:components_23_31`

3. The appendix support tables remain tied to the same representative cutoff, but in a supplementary role.
   - `tab:gamma_sigma_intervals1`
   - `tab:gamma_sigma_intervals2`

4. The historical-summary objects remain workflow-linked descriptive support and are frozen locally in the article repo.
   - `fig:dry_quantile`
   - `fig:rainy_quantile`
   - `fig:80_components`

5. The corrections letter is synchronized to the same provenance split and current benchmark table values.

## Audit status summary

### Established in this pass
- the benchmark table in the revised article is now aligned with the frozen HE2 publication manifest,
- the representative selected-model outputs are refreshed from verified `exAL-M-T1` sources,
- the appendix support tables are explicitly demoted to a supplementary role,
- the historical-summary figures are workflow-linked, hash-verified, and frozen locally in the revised article repo, and
- the corrections letter is synchronized to the current article-side provenance split.

### Remaining optional work
- further aesthetic or publication-quality refreshes of historical-summary figures, if ever desired, should be treated as optional figure-improvement work rather than as unresolved provenance work.
