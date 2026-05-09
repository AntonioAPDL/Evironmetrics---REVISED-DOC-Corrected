#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from article_asset_manifest import load_manifest

LEGACY_GENERATED_FAMILIES = [
    'historical_summary_sources',
    'workflow_linked_support_sources',
    'setup_support_by_cutoff',
    'setup_support_by_cutoff_review',
]

LEGACY_TOPLEVEL_DIRS = [
    'Figures',
]

LEGACY_SCRIPTS = [
    'scripts/refresh_local_provenance_bundles.py',
    'scripts/refresh_setup_support_by_cutoff.py',
    'scripts/build_setup_support_by_cutoff_review.py',
]


def tracked_disc_stale_files(article_root: Path, expected_disc: set[str]) -> list[str]:
    try:
        proc = subprocess.run(
            ['git', '-C', str(article_root), 'ls-files', 'DISC'],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return []
    out: list[str] = []
    for line in proc.stdout.splitlines():
        name = Path(line).name
        if name and name not in expected_disc:
            out.append(name)
    return sorted(set(out))


def remove_path(path: Path) -> bool:
    if not path.exists():
        return False
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()
    return True


def build_report(article_root: Path, removed_disc: list[str], removed_paths: list[str]) -> None:
    manifest = load_manifest(article_root)
    expected_disc = sorted(fig['filename'] for fig in manifest['figures'])
    generated_root = article_root / 'generated'
    kept_families = sorted(p.name for p in generated_root.iterdir() if p.is_dir())

    report_dir = generated_root / 'article_asset_review'
    report_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        'article_root': str(article_root),
        'canonical_disc_files': expected_disc,
        'removed_disc_files': removed_disc,
        'removed_legacy_paths': removed_paths,
        'retained_generated_families': kept_families,
    }
    (report_dir / 'article_repo_cleanup_audit.json').write_text(json.dumps(payload, indent=2) + '\n')

    md: list[str] = []
    md.append('# Article Repo Cleanup Audit\n\n')
    md.append('This report records the article-side cleanup that prunes legacy figure/table assets not used by the current manuscript and not wired to the current refresh workflow.\n\n')
    md.append('## Canonical manuscript-facing figures\n\n')
    for name in expected_disc:
        md.append(f'- `DISC/{name}`\n')
    md.append('\n## Removed stale `DISC/` files\n\n')
    md.append(f'- Count: `{len(removed_disc)}`\n')
    if removed_disc:
        for name in removed_disc:
            md.append(f'  - `{name}`\n')
    else:
        md.append('- None\n')
    md.append('\n## Removed legacy article-side paths\n\n')
    if removed_paths:
        for rel in removed_paths:
            md.append(f'- `{rel}`\n')
    else:
        md.append('- None\n')
    md.append('\n## Retained generated families\n\n')
    for fam in kept_families:
        md.append(f'- `generated/{fam}`\n')
    md.append('\n## Current cleanup contract\n\n')
    md.append('1. `DISC/` should contain only the figure files named in `ARTICLE_GENERATED_ASSET_MANIFEST.json`.\n')
    md.append('2. Legacy article-side figure families superseded by the current `v2` / current-output workflow should remain absent.\n')
    md.append('3. Refresh through `scripts/refresh_all_generated_assets.py`, which now re-applies this cleanup automatically.\n')
    (report_dir / 'ARTICLE_REPO_CLEANUP_AUDIT.md').write_text(''.join(md))


def main() -> None:
    parser = argparse.ArgumentParser(description='Prune stale article-side figure/table assets and legacy generated families.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    manifest = load_manifest(article_root)

    disc_root = article_root / 'DISC'
    expected_disc = {fig['filename'] for fig in manifest['figures']}
    removed_disc: list[str] = tracked_disc_stale_files(article_root, expected_disc)
    if disc_root.exists():
        for path in sorted(disc_root.iterdir()):
            if path.is_file() and path.name not in expected_disc:
                path.unlink()
                if path.name not in removed_disc:
                    removed_disc.append(path.name)
    removed_disc = sorted(set(removed_disc))

    removed_paths: list[str] = []
    for rel in LEGACY_GENERATED_FAMILIES:
        if remove_path(article_root / 'generated' / rel):
            removed_paths.append(f'generated/{rel}')
    for rel in LEGACY_TOPLEVEL_DIRS:
        if remove_path(article_root / rel):
            removed_paths.append(rel)
    for rel in LEGACY_SCRIPTS:
        if remove_path(article_root / rel):
            removed_paths.append(rel)

    build_report(article_root, removed_disc, removed_paths)
    print(f'Removed {len(removed_disc)} stale DISC files and {len(removed_paths)} legacy paths.')


if __name__ == '__main__':
    main()
