#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from article_asset_manifest import load_manifest, manifest_path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description='Promote manuscript figures into DISC/ from the source-controlled generated-asset manifest.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    manifest = load_manifest(article_root)
    disc_root = article_root / 'DISC'
    disc_root.mkdir(parents=True, exist_ok=True)
    out_root = article_root / 'generated' / 'article_asset_selection'
    out_root.mkdir(parents=True, exist_ok=True)

    expected = {fig['filename'] for fig in manifest['figures']}
    for stale in sorted(disc_root.iterdir()):
        if stale.is_file() and stale.name not in expected:
            stale.unlink()

    rows: list[dict[str, object]] = []
    for fig in manifest['figures']:
        src = article_root / fig['generated_source']
        if not src.exists():
            raise FileNotFoundError(f'Missing generated source for {fig["label"]}: {src}')
        dst = disc_root / fig['filename']
        shutil.copy2(src, dst)
        rows.append({
            'label': fig['label'],
            'filename': fig['filename'],
            'category': fig['category'],
            'role': fig['role'],
            'source_class': fig['source_class'],
            'current_model_output_wired': bool(fig['current_model_output_wired']),
            'generated_source': fig['generated_source'],
            'disc_target': f'DISC/{fig["filename"]}',
            'sha256': sha256(dst),
            'note': fig['note'],
        })

    selection = {
        'manifest_path': str(manifest_path(article_root)),
        'disc_root': str(disc_root),
        'figures': rows,
    }
    (out_root / 'selection_manifest.json').write_text(json.dumps(selection, indent=2) + '\n')
    (out_root / 'README.md').write_text(
        '# Article Figure Selection Manifest\n\n'
        'This directory records the exact generated-asset sources currently promoted into `DISC/`.\n\n'
        'Refresh path:\n'
        '- `scripts/promote_generated_figures_to_disc.py`\n\n'
        'The source-controlled selection rules live in:\n'
        f'- `{manifest_path(article_root).name}`\n'
    )
    print(f'Promoted {len(rows)} figures into {disc_root}')


if __name__ == '__main__':
    main()
