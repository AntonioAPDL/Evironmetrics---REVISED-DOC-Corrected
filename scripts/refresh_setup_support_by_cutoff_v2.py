#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from article_repo_layout import build_layout


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> None:
    parser = argparse.ArgumentParser(description='Refresh the article-side five-cutoff setup/support artifact bundle from the workflow runtime family.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--workflow-runtime-root', type=Path, default=Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/exal_m_t1_setup_support_by_cutoff_v2_20260507'))
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    runtime_root = args.workflow_runtime_root.resolve()
    if not runtime_root.exists():
        raise FileNotFoundError(f'Missing workflow runtime bundle: {runtime_root}')

    layout = build_layout(article_root)
    layout.ensure_base_dirs()
    dest_root = layout.five_cutoff_setup_support_dir
    copy_tree(runtime_root, dest_root)
    print(f'Refreshed five-cutoff setup/support bundle into {dest_root}')


if __name__ == '__main__':
    main()
