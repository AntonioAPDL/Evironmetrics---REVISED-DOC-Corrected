# Generated Asset Index

This directory is the article-side freeze point for generated figures, tables, manifests, and audit bundles used by the revised manuscript.

Primary article repo:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/Evironmetrics---REVISED-DOC-2`

Preferred refresh entrypoint:
- `scripts/refresh_all_generated_assets.py`

Companion workflow runbook:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/CANONICAL_REVISED_ARTICLE_WORKFLOW.md`

Future full-history repair plan:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/HE2_FULL_HISTORY_REPAIR_FORWARD_PLAN.md`

## Asset families

| Family | Description | Files | PNGs | README | Review entrypoints |
|---|---|---:|---:|---|---|
| `article_asset_review` | Top-level review report, gallery, and wiring audit for current article figures and tables. | 7 | 0 | no | `ARTICLE_ASSET_REVIEW.md` |
| `article_asset_selection` | Manifest showing which generated figure files are currently promoted into DISC/. | 2 | 0 | yes | `README.md` |
| `article_table_includes` | Generated TeX row includes for the manuscript tables, rebuilt from frozen article-side data sources. | 13 | 0 | yes | `README.md` |
| `current_model_output_support` | Canonical current-output support bundle for manuscript historical summaries and supporting appendix figures. | 14 | 5 | yes | `README.md` |
| `exal_m_t1_20221225` | Representative selected-model bundle from the verified 2022-12-25 exAL-M-T1 rerun. | 26 | 3 | yes | `README.md` |
| `exal_m_t1_five_run_sources` | Five-cutoff publication source freeze for exAL-M-T1. | 18 | 0 | yes | `README.md` |
| `he2_historical_support_audit_20260507` | Audit snapshot showing which published Bayesian rows use full historical support versus short-window support. | 3 | 0 | yes | `README.md` |
| `he2_publication_manifest_snapshot` | Frozen local snapshot of the current HE2 Bayesian publication manifest and alignment tables. | 7 | 0 | yes | `README.md` |
| `setup_support_by_cutoff_v2` | Canonical cutoff-specific setup/support figure family mirrored from the validated v2 workflow. | 74 | 20 | yes | `review/gallery.html | README.md` |
| `setup_support_by_cutoff_v2_appendix` | Appendix-ready composite panels built from the canonical v2 cutoff-specific setup/support figure family. | 7 | 5 | yes | `README.md` |
| `setup_support_by_cutoff_v2_article_selection` | Manifest for which cutoff-specific v2 figures are promoted into DISC/. | 1 | 0 | no | `` |
| `setup_support_by_cutoff_v2_review` | Review markdown/gallery and audits for the canonical v2 setup/support figure family. | 6 | 0 | no | `SETUP_SUPPORT_BY_CUTOFF_V2_REVIEW.md | INPUT_ALIGNMENT_AUDIT.md | gallery.html` |

## Working rules

1. Refresh generated bundles through article-side scripts rather than manual copying.
2. Treat `generated/` as the manuscript-local freeze point, not the authoritative build factory.
3. Keep workflow-side source-of-truth manifests and runbooks in the workflow repo.
4. Promote files into `DISC/` only from a generated family with a manifest or review trail.
5. When future reruns change model outputs, refresh the generated families first and only then update manuscript-facing files.

## Important note

The current publication state and the future corrected full-history rerun state must remain separate until a deliberate update is made.
