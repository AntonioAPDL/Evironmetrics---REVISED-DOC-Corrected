#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print('+', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description='Refresh all article-side generated assets and reports.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--workflow-root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--runtime-root', type=Path, default=Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_publication_replay_representatives_20260506'))
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    workflow_root = args.workflow_root.resolve()
    runtime_root = args.runtime_root.resolve()

    py = sys.executable
    run([py, str(article_root / 'scripts' / 'refresh_current_model_output_support_figures.py'), '--article-root', str(article_root), '--workflow-root', str(workflow_root)])
    run([py, str(article_root / 'scripts' / 'refresh_exal_m_t1_generated_assets.py'), '--article-root', str(article_root), '--runtime-root', str(runtime_root)])
    run([py, str(article_root / 'scripts' / 'refresh_he2_manifest_snapshot.py'), '--article-root', str(article_root), '--workflow-root', str(workflow_root)])
    run([py, str(article_root / 'scripts' / 'refresh_setup_support_by_cutoff_v2.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_setup_support_by_cutoff_v2_review.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_setup_support_transform_lineage_audit.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_setup_support_by_cutoff_v2_appendix.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'promote_setup_support_v2_to_disc.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_generated_table_includes.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'promote_generated_figures_to_disc.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_article_asset_review_report.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'clean_article_legacy_assets.py'), '--article-root', str(article_root)])
    run([py, str(article_root / 'scripts' / 'build_generated_asset_index.py'), '--article-root', str(article_root)])
    print('Refreshed all article-side generated assets successfully.')


if __name__ == '__main__':
    main()
