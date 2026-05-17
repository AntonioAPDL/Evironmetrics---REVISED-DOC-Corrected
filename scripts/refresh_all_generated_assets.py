#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def run_optional(cmd: list[str], status_path: Path, *, strict: bool) -> None:
    print('+', ' '.join(cmd))
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    status_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        'command': cmd,
        'returncode': proc.returncode,
        'stdout': proc.stdout,
        'stderr': proc.stderr,
        'status': 'ok' if proc.returncode == 0 else 'skipped',
    }
    status_path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    if proc.returncode == 0:
        if proc.stdout:
            print(proc.stdout, end='')
        if proc.stderr:
            print(proc.stderr, end='', file=sys.stderr)
        return
    if strict:
        if proc.stdout:
            print(proc.stdout, end='')
        if proc.stderr:
            print(proc.stderr, end='', file=sys.stderr)
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)
    print(
        'WARNING: current-model support refresh skipped; see '
        f'{status_path} for the captured failure and the retained artifact state.',
        file=sys.stderr,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description='Refresh all article-side generated assets and reports.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--workflow-root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--runtime-root', type=Path, default=Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_multivar_keep_all_cutoffs_20260512'))
    parser.add_argument('--univar-runtime-root', type=Path, default=Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_univar_featurecov_he2_rerun_20260422'))
    parser.add_argument(
        '--strict-current-model-support',
        action='store_true',
        help='Fail the full refresh if the current-model historical-support refresh cannot be rebuilt from the configured runtime roots.',
    )
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    workflow_root = args.workflow_root.resolve()
    runtime_root = args.runtime_root.resolve()
    univar_runtime_root = args.univar_runtime_root.resolve()

    py = sys.executable
    run_optional([
        py,
        str(article_root / 'scripts' / 'refresh_current_model_output_support_figures.py'),
        '--article-root',
        str(article_root),
        '--workflow-root',
        str(workflow_root),
        '--multivar-runtime-root',
        str(runtime_root),
        '--univar-runtime-root',
        str(univar_runtime_root),
    ], article_root / 'artifacts' / 'historical_support_from_current_models' / 'refresh_status.json', strict=args.strict_current_model_support)
    run([py, str(article_root / 'scripts' / 'refresh_exal_m_t1_generated_assets.py'), '--article-root', str(article_root), '--runtime-root', str(runtime_root)])
    run([
        py,
        str(article_root / 'scripts' / 'refresh_cutoff_synthesis_families.py'),
        '--article-root',
        str(article_root),
        '--multivar-runtime-root',
        str(runtime_root),
        '--univar-runtime-root',
        str(univar_runtime_root),
    ])
    run([py, str(article_root / 'scripts' / 'refresh_he2_manifest_snapshot.py'), '--article-root', str(article_root), '--workflow-root', str(workflow_root)])
    run([py, str(article_root / 'scripts' / 'refresh_setup_support_by_cutoff_v2.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_setup_support_by_cutoff_v2_review.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_setup_support_transform_lineage_audit.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_setup_support_by_cutoff_v2_appendix.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'promote_cutoff_forecast_context_figures.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'promote_setup_support_v2_to_disc.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_generated_table_includes.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'promote_generated_figures_to_disc.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_article_asset_review_report.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_figure_polish_status_audit.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'clean_article_legacy_assets.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_generated_asset_index.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'validate_manuscript_figure_paths.py'), '--article-root', str(article_root)])
    print('Refreshed all article-side generated assets successfully.')


if __name__ == '__main__':
    main()
