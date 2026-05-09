#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

FAMILY_DESCRIPTIONS = {
    'article_asset_review': 'Top-level review report, gallery, and wiring audit for current article figures and tables.',
    'article_asset_selection': 'Manifest showing which generated figure files are currently promoted into DISC/.',
    'article_table_includes': 'Generated TeX row includes for the manuscript tables, rebuilt from frozen article-side data sources.',
    'exal_m_t1_20221225': 'Representative selected-model bundle from the verified 2022-12-25 exAL-M-T1 rerun.',
    'exal_m_t1_five_run_sources': 'Five-cutoff publication source freeze for exAL-M-T1.',
    'he2_historical_support_audit_20260507': 'Audit snapshot showing which published Bayesian rows use full historical support versus short-window support.',
    'he2_publication_manifest_snapshot': 'Frozen local snapshot of the current HE2 Bayesian publication manifest and alignment tables.',
    'current_model_output_support': 'Canonical current-output support bundle for manuscript historical summaries and supporting appendix figures.',
    'setup_support_by_cutoff_v2': 'Canonical cutoff-specific setup/support figure family mirrored from the validated v2 workflow.',
    'setup_support_by_cutoff_v2_appendix': 'Appendix-ready composite panels built from the canonical v2 cutoff-specific setup/support figure family.',
    'setup_support_by_cutoff_v2_article_selection': 'Manifest for which cutoff-specific v2 figures are promoted into DISC/.',
    'setup_support_by_cutoff_v2_review': 'Review markdown/gallery and audits for the canonical v2 setup/support figure family.',
}

PREFERRED_REVIEW_FILES = [
    'ARTICLE_ASSET_REVIEW.md',
    'SETUP_SUPPORT_BY_CUTOFF_V2_REVIEW.md',
    'SETUP_SUPPORT_BY_CUTOFF_V2_REVIEW.md',
    'SETUP_SUPPORT_BY_CUTOFF_REVIEW.md',
    'INPUT_ALIGNMENT_AUDIT.md',
    'gallery.html',
    'README.md',
]


def count_files(root: Path) -> int:
    return sum(1 for p in root.rglob('*') if p.is_file())


def count_png(root: Path) -> int:
    return sum(1 for p in root.rglob('*.png') if p.is_file())


def pick_review_targets(root: Path) -> list[str]:
    picks: list[str] = []
    for name in PREFERRED_REVIEW_FILES:
        for p in sorted(root.rglob(name)):
            rel = p.relative_to(root)
            s = str(rel)
            if s not in picks:
                picks.append(s)
    return picks[:6]


def main() -> None:
    parser = argparse.ArgumentParser(description='Build an index of article-side generated asset families.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    generated_root = article_root / 'generated'
    families = [p for p in sorted(generated_root.iterdir()) if p.is_dir()]

    rows = []
    for family in families:
        rows.append({
            'family': family.name,
            'path': str(family),
            'description': FAMILY_DESCRIPTIONS.get(family.name, 'Generated asset family.'),
            'file_count': count_files(family),
            'png_count': count_png(family),
            'has_readme': 'yes' if (family / 'README.md').exists() else 'no',
            'review_targets': ' | '.join(pick_review_targets(family)),
        })

    csv_path = generated_root / 'asset_inventory.csv'
    with csv_path.open('w', newline='') as f:
        fieldnames = ['family', 'path', 'description', 'file_count', 'png_count', 'has_readme', 'review_targets']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    md: list[str] = []
    md.append('# Generated Asset Index\n\n')
    md.append('This directory is the article-side freeze point for generated figures, tables, manifests, and audit bundles used by the revised manuscript.\n\n')
    md.append('Primary article repo:\n')
    md.append(f'- `{article_root}`\n\n')
    md.append('Preferred refresh entrypoint:\n')
    md.append('- `scripts/refresh_all_generated_assets.py`\n\n')
    md.append('Companion workflow runbook:\n')
    md.append('- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/CANONICAL_REVISED_ARTICLE_WORKFLOW.md`\n\n')
    md.append('Future full-history repair plan:\n')
    md.append('- `/data/muscat_data/jaguir26/project1_ucsc_phd/repro/run/HE2_FULL_HISTORY_REPAIR_FORWARD_PLAN.md`\n\n')
    md.append('## Asset families\n\n')
    md.append('| Family | Description | Files | PNGs | README | Review entrypoints |\n')
    md.append('|---|---|---:|---:|---|---|\n')
    for row in rows:
        md.append(
            f"| `{row['family']}` | {row['description']} | {row['file_count']} | {row['png_count']} | {row['has_readme']} | `{row['review_targets']}` |\n"
        )
    md.append('\n## Working rules\n\n')
    md.append('1. Refresh generated bundles through article-side scripts rather than manual copying.\n')
    md.append('2. Treat `generated/` as the manuscript-local freeze point, not the authoritative build factory.\n')
    md.append('3. Keep workflow-side source-of-truth manifests and runbooks in the workflow repo.\n')
    md.append('4. Promote files into `DISC/` only from a generated family with a manifest or review trail.\n')
    md.append('5. When future reruns change model outputs, refresh the generated families first and only then update manuscript-facing files.\n')
    md.append('\n## Important note\n\n')
    md.append('The current publication state and the future corrected full-history rerun state must remain separate until a deliberate update is made.\n')
    (generated_root / 'README.md').write_text(''.join(md))


if __name__ == '__main__':
    main()
