# exAL-M-T1 Shared Rerun Checklist

Date: 2026-05-16

## Purpose

This note records the **next** `exAL-M-T1` relaunch target for the revised article.

It does not replace the already-frozen publication-state provenance in:
- `docs/exal_m_t1_relaunch_checklist.md`
- `docs/exal_m_t1_artifact_run_map.md`

Instead, it defines the staged rerun/update contract we will use to replace the current
`20260512` `exdqlm_multivar_keep` article-facing bundles once the new shared relaunch
is completed and revalidated.

Primary workflow-side plan:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/HE2_EXDQLM_MULTIVAR_KEEP_SHARED_RELAUNCH_PLAN_20260516.md`

Primary workflow-side shared-spec report:
- `/data/muscat_data/jaguir26/project1_ucsc_phd/reports/he2_exdqlm_multivar_keep_shared_relaunch_plan_20260516/HE2_EXDQLM_MULTIVAR_KEEP_SHARED_RELAUNCH_PLAN_20260516.md`

## Current article status

Right now the revised article is still wired to the completed `20260512` corrected
five-cutoff relaunch family and its associated support bundles.

That remains the current manuscript-side provenance anchor until the shared rerun exists
and is validated.

So the article repo has two states we need to keep separate:

1. the **current published-state freeze** already mirrored locally
2. the **next shared rerun target** that is prepared but not yet executed

## Locked shared rerun spec

The next relaunch is planned around a single shared `exAL-M-T1` spec:

| Contract item | Locked choice |
|---|---|
| family | `exdqlm_multivar_keep` |
| cutoffs | `20210123`, `20211112`, `20211221`, `20220511`, `20221225` |
| retros / USGS window | `1987-05-29 -> cutoff` |
| shared bundle lineage | `multimodel_v8_he2_publication_shared_inputs_20260510` |
| bundle run id | `20260510_publication_shared_r01` |
| deterministic blended covariates | `PPT`, `SOIL` |
| climate factor alias | `PCA` backed by canonical `GDPC1` |
| shared `epsilon` | `360.0` |
| shared `c_factor` | `1.0` |
| shared discount set | `set08` |
| shared q50 stabilization | `freeze_target=states`, `hold_after_guard=0`, blend `0.5/0.5`, step caps `0.15/0.25`, `fail_fast` guard |

## Figure / table families to refresh after the rerun

These are the article-side bundles that must be refreshed from the **new** shared rerun outputs,
not the current `20260512` root:

| Article family | Role | Refresh stage |
|---|---|---|
| `artifacts/five_cutoff_crps_validation_sources/` | Table 1 CRPS source freeze | after rerun row reports pass |
| `artifacts/representative_selected_model_2022_12_25/` | representative Section 5 bundle | after rerun row reports pass |
| `artifacts/five_cutoff_setup_support/` | cutoff-specific setup/input/support figures | after article refresh stage starts |
| `figures/forecast_context_by_cutoff/` | all-cutoff forecast-window context figures | after article refresh stage starts |
| `figures/multivariate_synthesis_by_cutoff/` | all-cutoff main-model synthesis figures | after article refresh stage starts |
| `figures/reference_synthesis_by_cutoff/` | all-cutoff reference synthesis figures | after article refresh stage starts |
| `artifacts/historical_support_from_current_models/` | historical support figures | only if the retained-artifact contract is satisfied |

## Staged execution schedule

### Stage A: no-launch validation

The workflow repo must first complete:
- shared-spec config build
- prelaunch validator
- representative q50/q65 execution smokes

No article assets should be refreshed from the planned shared runtime root before this stage passes.

### Stage B: relaunch execution

The workflow repo then performs:
1. canary relaunch rows
2. full five-cutoff relaunch
3. row-level `fit`, `post`, `validate`, `report` checks

### Stage C: article refresh

Only after Stage B passes should the revised-doc repo refresh:
1. five-cutoff CRPS freeze
2. representative selected-model bundle
3. setup/support by cutoff
4. forecast-context by cutoff
5. multivariate synthesis by cutoff
6. reference synthesis by cutoff
7. manuscript figure/table review manifests

### Stage D: Overleaf handoff

After the article-side refresh is complete:
1. validate generated figure/table paths
2. commit article-side bundle updates
3. push the revised-doc branch
4. pull into Overleaf

## Operator rule

Until the shared rerun is complete:

- keep treating `docs/exal_m_t1_relaunch_checklist.md` as the current article provenance
- treat this file as the **planned next-state contract**
- do not mix the two in manuscript claims
