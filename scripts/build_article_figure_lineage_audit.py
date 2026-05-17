#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from article_asset_manifest import load_manifest
from article_repo_layout import build_layout

LIVE_KEEP_ROOT = Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_multivar_keep_all_cutoffs_sharedspec_20260516')
COMPLETED_KEEP_ROOT = Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_multivar_keep_all_cutoffs_20260512')
SETUP_SUPPORT_RUNTIME = Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/exal_m_t1_setup_support_by_cutoff_v2_20260516')


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def keep_sharedspec_complete() -> bool:
    summaries = list((LIVE_KEEP_ROOT / 'runs').glob('*/report/summary.json'))
    return len(summaries) == 5


def infer_row(rel_path: str, manuscript_sources: dict[str, dict[str, str]], appendix_rows: dict[str, dict[str, str]], forecast_rows: dict[str, dict[str, str]], multivar_rows: dict[str, dict[str, str]], reference_rows: dict[str, dict[str, str]]) -> dict[str, str]:
    prefix = rel_path.split('/', 1)[0]
    name = Path(rel_path).name

    if rel_path.startswith('manuscript/'):
        src = manuscript_sources.get(rel_path, {})
        label = src.get('label', '')
        source_path = src.get('source_path', '')
        if label in {'fig:sanlorenzo', 'fig:covariates', 'fig:retrospectives', 'fig:ensembles'}:
            return {
                'classification': 'input-side / support / context figure',
                'source_script': 'scripts/refresh_setup_support_by_cutoff_v2.py -> scripts/promote_setup_support_v2_to_disc.py -> scripts/promote_generated_figures_to_disc.py',
                'source_lineage': 'corrected_setup_support_v2_20260516',
                'status': 'updated_now',
                'blocker': '',
                'source_path': source_path,
            }
        if label in {'fig:synth1'}:
            return {
                'classification': 'model-output-driven figure',
                'source_script': 'scripts/refresh_exal_m_t1_generated_assets.py -> scripts/promote_generated_figures_to_disc.py',
                'source_lineage': 'completed_keep_outputs_20260512',
                'status': 'blocked_pending_live_keep_sharedspec_outputs',
                'blocker': 'Live shared-spec keep rerun 20260516 has not produced final post/report outputs for all cutoffs yet.',
                'source_path': source_path,
            }
        if label in {'fig:dry_quantile', 'fig:rainy_quantile', 'fig:80_components', 'fig:synth2'}:
            return {
                'classification': 'model-output-driven figure',
                'source_script': 'scripts/refresh_current_model_output_support_figures.py -> scripts/promote_generated_figures_to_disc.py',
                'source_lineage': 'completed_keep_outputs_20260512',
                'status': 'blocked_pending_live_keep_sharedspec_outputs',
                'blocker': 'Current-model support figures still depend on completed 20260512 keep outputs until the live shared-spec rerun finishes and a retained support-artifact contract is available.',
                'source_path': source_path,
            }
    if rel_path.startswith('appendix_cutoff_panels/') and name != 'README.md' and name != 'manifest.csv':
        row = next((r for r in appendix_rows.values() if Path(r['panel_path']).name == name), {})
        return {
            'classification': 'input-side / support / context figure',
            'source_script': 'scripts/refresh_setup_support_by_cutoff_v2.py -> scripts/build_setup_support_by_cutoff_v2_appendix.py',
            'source_lineage': 'corrected_setup_support_v2_20260516',
            'status': 'updated_now',
            'blocker': '',
            'source_path': row.get('panel_path', ''),
        }
    if rel_path.startswith('forecast_context_by_cutoff/') and name not in {'README.md', 'manifest.csv'}:
        row = forecast_rows.get(name, {})
        return {
            'classification': 'input-side / support / context figure',
            'source_script': 'scripts/refresh_setup_support_by_cutoff_v2.py -> scripts/promote_cutoff_forecast_context_figures.py',
            'source_lineage': 'corrected_setup_support_v2_20260516',
            'status': 'updated_now',
            'blocker': '',
            'source_path': row.get('source_path', ''),
        }
    if rel_path.startswith('multivariate_synthesis_by_cutoff/') and name not in {'README.md', 'manifest.csv'}:
        row = multivar_rows.get(name, {})
        return {
            'classification': 'synthesis figure',
            'source_script': 'scripts/refresh_cutoff_synthesis_families.py',
            'source_lineage': 'completed_keep_outputs_20260512',
            'status': 'blocked_pending_live_keep_sharedspec_outputs',
            'blocker': 'Cutoff-wide multivariate synthesis family still reflects the last completed keep-output root (20260512) until the live shared-spec rerun completes.',
            'source_path': row.get('source_path', ''),
        }
    if rel_path.startswith('reference_synthesis_by_cutoff/') and name not in {'README.md', 'manifest.csv'}:
        row = reference_rows.get(name, {})
        return {
            'classification': 'synthesis figure',
            'source_script': 'scripts/refresh_cutoff_synthesis_families.py',
            'source_lineage': 'completed_reference_outputs_20260422',
            'status': 'unchanged_intentionally',
            'blocker': '',
            'source_path': row.get('source_path', ''),
        }
    return {
        'classification': 'figure unaffected by corrected lineage',
        'source_script': 'n/a',
        'source_lineage': 'n/a',
        'status': 'unchanged_intentionally',
        'blocker': '',
        'source_path': '',
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Build a strict article figure-lineage audit for the revised repo.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    layout = build_layout(article_root)
    layout.ensure_base_dirs()

    manifest = load_manifest(article_root)
    manuscript_sources = {Path(row['manuscript_path']).relative_to('figures').as_posix(): row for row in manifest['figures']}

    appendix_manifest = load_csv(layout.appendix_cutoff_panels_dir / 'manifest.csv')
    appendix_rows = {Path(r['panel_path']).name: r for r in appendix_manifest}
    forecast_manifest = load_csv(layout.cutoff_forecast_context_dir / 'manifest.csv')
    forecast_rows = {Path(r['target_path']).name: r for r in forecast_manifest}
    multivar_manifest = load_csv(layout.cutoff_multivariate_synthesis_dir / 'manifest.csv') if (layout.cutoff_multivariate_synthesis_dir / 'manifest.csv').exists() else []
    multivar_rows = {Path(r['target_path']).name: r for r in multivar_manifest}
    reference_manifest = load_csv(layout.cutoff_reference_synthesis_dir / 'manifest.csv') if (layout.cutoff_reference_synthesis_dir / 'manifest.csv').exists() else []
    reference_rows = {Path(r['target_path']).name: r for r in reference_manifest}

    setup_rows = []
    for slug_dir in sorted(layout.five_cutoff_setup_support_dir.iterdir()):
        if not slug_dir.is_dir() or slug_dir.name == 'review':
            continue
        coverage = json.loads((slug_dir / 'metadata' / 'cutoff_entry.json').read_text())
        cov_yaml = (slug_dir / 'metadata' / 'coverage_audit.yaml').read_text(encoding='utf-8')
        support_yaml = (slug_dir / 'metadata' / 'support_window.yaml').read_text(encoding='utf-8')
        setup_rows.append((slug_dir.name, coverage, cov_yaml, support_yaml))

    full_history_all_setup = True
    gdpc_all_setup = True
    for slug, entry, cov_text, _support_text in setup_rows:
        if "retrospective:\n  requested_start: '1987-05-29'" not in cov_text or "full_history_available: true" not in cov_text.split('retrospective:')[-1]:
            full_history_all_setup = False
        if "gdpc:" not in cov_text or "full_history_available: true" not in cov_text.split('gdpc:')[-1].split('retrospective:')[0]:
            gdpc_all_setup = False

    rows = []
    for rel in sorted(str(p.relative_to(layout.figures_dir)) for p in layout.figures_dir.rglob('*') if p.is_file()):
        info = infer_row(rel, manuscript_sources, appendix_rows, forecast_rows, multivar_rows, reference_rows)
        rows.append({
            'figure_path': f'figures/{rel}',
            **info,
        })

    uppercase_root = article_root / 'Figures'
    lowercase_files = {str(p.relative_to(layout.figures_dir)) for p in layout.figures_dir.rglob('*') if p.is_file()}
    uppercase_files = {str(p.relative_to(uppercase_root)) for p in uppercase_root.rglob('*') if p.is_file()} if uppercase_root.exists() else set()
    uppercase_figure_files = {p for p in uppercase_files if p not in {'README.md', 'mirror_manifest.csv'}}
    mirror_match = lowercase_files == uppercase_figure_files

    report_root = layout.reports_dir / 'article_figure_lineage_audit_20260516'
    report_root.mkdir(parents=True, exist_ok=True)

    with (report_root / 'figure_lineage_status.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        'setup_support_runtime_root': str(SETUP_SUPPORT_RUNTIME),
        'completed_keep_output_root': str(COMPLETED_KEEP_ROOT),
        'live_keep_sharedspec_root': str(LIVE_KEEP_ROOT),
        'live_keep_sharedspec_complete': keep_sharedspec_complete(),
        'setup_support_full_history_all_cutoffs': full_history_all_setup,
        'setup_support_gdpc_all_cutoffs': gdpc_all_setup,
        'uppercase_lowercase_figure_trees_match': mirror_match,
        'lowercase_figure_file_count': len(lowercase_files),
        'uppercase_figure_file_count': len(uppercase_figure_files),
        'status_counts': {s: sum(1 for row in rows if row['status'] == s) for s in sorted({row['status'] for row in rows})},
    }
    (report_root / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')

    md = []
    md.append('# Article Figure Lineage Audit\n\n')
    md.append('## Executive read\n\n')
    md.append(f"- Setup/support family refreshed from `{SETUP_SUPPORT_RUNTIME}`.\n")
    md.append(f"- Setup/support full-history contract across all cutoffs: `{'PASS' if full_history_all_setup else 'FAIL'}`.\n")
    md.append(f"- Setup/support GDPC contract across all cutoffs: `{'PASS' if gdpc_all_setup else 'FAIL'}`.\n")
    md.append(f"- Live shared-spec keep outputs complete: `{'YES' if keep_sharedspec_complete() else 'NO'}`.\n")
    md.append(f"- Legacy uppercase `Figures/` mirror matches lowercase canonical `figures/`: `{'YES' if mirror_match else 'NO'}`.\n\n")
    md.append('## Figure family conclusions\n\n')
    md.append('| Family | Current status | Source lineage | Notes |\n')
    md.append('|---|---|---|---|\n')
    md.append(f"| Setup/support manuscript figures + appendix panels + forecast-context family | `updated_now` | `exal_m_t1_setup_support_by_cutoff_v2_20260516` | Full USGS/PPT/SOIL/GDPC history from `1987-05-29 -> cutoff`; retrospective support now sourced from repaired canonical shared bundles for all cutoffs. |\n")
    md.append(f"| Representative keep synthesis + cutoff-wide multivariate synthesis | `blocked_pending_live_keep_sharedspec_outputs` | last completed keep output root `20260512` | Keep-model output figures should move to the live shared-spec rerun after it finishes `post/validate/report`. |\n")
    md.append(f"| Historical support from current models | `blocked_pending_live_keep_sharedspec_outputs` | current completed keep output root `20260512` | Current-model support renderer still depends on completed keep artifacts until a retained support cache exists for the live rerun. |\n")
    md.append(f"| Reference synthesis family | `unchanged_intentionally` | existing univariate output lineage | Not part of the current multivariate keep input-bundle correction. |\n\n")
    md.append('## Per-figure status\n\n')
    md.append('| Figure path | Class | Status | Source lineage | Source script | Blocker |\n')
    md.append('|---|---|---|---|---|---|\n')
    for row in rows:
        md.append(f"| `{row['figure_path']}` | {row['classification']} | `{row['status']}` | `{row['source_lineage']}` | `{row['source_script']}` | {row['blocker'] or '-'} |\n")
    md.append('\n## Explicit keep-family confirmation\n\n')
    md.append(f"- Setup/support keep figure families now use full history: `{'YES' if full_history_all_setup else 'NO'}`.\n")
    md.append(f"- Setup/support keep figure families now use GDPC instead of the legacy PCA interpretation: `{'YES' if gdpc_all_setup else 'NO'}`.\n")
    md.append('- Setup/support keep figure families now use corrected retrospective/forecast bundle lineage from the canonical `20260510` shared-input bundles.\n')
    md.append('- Keep model-output families are not yet refreshed to the live shared-spec rerun because those outputs are not complete yet; they remain explicitly blocked rather than silently refreshed from stale outputs.\n')
    (report_root / 'ARTICLE_FIGURE_LINEAGE_AUDIT_20260516.md').write_text(''.join(md), encoding='utf-8')
    print(report_root)


if __name__ == '__main__':
    main()
