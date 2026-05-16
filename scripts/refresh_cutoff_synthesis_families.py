#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path

from article_repo_layout import (
    CUTOFF_MULTIVARIATE_SYNTHESIS_FILENAMES,
    CUTOFF_MULTIVARIATE_SYNTHESIS_OVERLAY_FILENAMES,
    CUTOFF_REFERENCE_SYNTHESIS_FILENAMES,
    CUTOFF_REFERENCE_SYNTHESIS_OVERLAY_FILENAMES,
    build_layout,
)

CUTOFF_SPECS = [
    {
        'slug': '20210123_exal_m_t1',
        'cutoff': '2021-01-23',
        'multivar_run_id': 'multimodel_20210123_v8_he2pubgdpc1r1_exdqlm_multivar_keep',
        'univar_run_id': 'multimodel_20210123_v8_univar_featurecov_he2_v1_exdqlm_univar',
    },
    {
        'slug': '20211112_exal_m_t1',
        'cutoff': '2021-11-12',
        'multivar_run_id': 'multimodel_20211112_v8_he2pubgdpc1r1_exdqlm_multivar_keep',
        'univar_run_id': 'multimodel_20211112_v8_univar_featurecov_he2_v1_exdqlm_univar',
    },
    {
        'slug': '20211221_exal_m_t1',
        'cutoff': '2021-12-21',
        'multivar_run_id': 'multimodel_20211221_v8_he2pubgdpc1r1_exdqlm_multivar_keep',
        'univar_run_id': 'multimodel_20211221_v8_univar_featurecov_he2_v1_exdqlm_univar',
    },
    {
        'slug': '20220511_exal_m_t1',
        'cutoff': '2022-05-11',
        'multivar_run_id': 'multimodel_20220511_v8_he2pubgdpc1r1_exdqlm_multivar_keep',
        'univar_run_id': 'multimodel_20220511_v8_univar_featurecov_he2_v1_exdqlm_univar',
    },
    {
        'slug': '20221225_exal_m_t1',
        'cutoff': '2022-12-25',
        'multivar_run_id': 'multimodel_20221225_v8_he2pubgdpc1r1_exdqlm_multivar_keep',
        'univar_run_id': 'multimodel_20221225_v8_univar_featurecov_he2_v1_exdqlm_univar',
    },
]

MULTIVAR_FILES = [
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples.png',
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples.pdf',
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples_with_raw_ensembles.png',
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples_with_raw_ensembles.pdf',
    'exdqlm_multivar_synth_keep_cutoff_window_quantiles.csv',
    'exdqlm_multivar_synth_keep_cutoff_window_sample_subset.csv',
    'publication_figure_manifest.csv',
    'publication_style_used.yaml',
]

UNIVAR_FILES = [
    'exdqlm_univar_synth_cutoff_window_posterior_samples.png',
    'exdqlm_univar_synth_cutoff_window_posterior_samples.pdf',
    'exdqlm_univar_synth_cutoff_window_posterior_samples_with_raw_ensembles.png',
    'exdqlm_univar_synth_cutoff_window_posterior_samples_with_raw_ensembles.pdf',
    'exdqlm_univar_synth_cutoff_window_quantiles.csv',
    'exdqlm_univar_synth_cutoff_window_sample_subset.csv',
    'publication_figure_manifest.csv',
    'publication_style_used.yaml',
]


def sha256sum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_file(src: Path, dst: Path) -> dict[str, str | int]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return {
        'source_path': str(src),
        'target_path': str(dst),
        'sha256': sha256sum(dst),
        'bytes': dst.stat().st_size,
    }


def _source_output_roots(multivar_runtime_root: Path, univar_runtime_root: Path, spec: dict[str, str]) -> tuple[Path, Path]:
    multivar_root = (
        multivar_runtime_root
        / 'runs'
        / spec['multivar_run_id']
        / 'post'
        / 'outputs'
        / spec['multivar_run_id']
    )
    univar_root = (
        univar_runtime_root
        / 'runs'
        / spec['univar_run_id']
        / 'post'
        / 'outputs'
        / spec['univar_run_id']
    )
    return multivar_root, univar_root


def _write_bundle(
    bundle_root: Path,
    *,
    family_name: str,
    source_run_id: str,
    source_output_root: Path,
    files: list[str],
) -> list[dict[str, str | int]]:
    bundle_root.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str | int]] = []
    for rel in files:
        meta = copy_file(source_output_root / rel, bundle_root / Path(rel).name)
        rows.append(
            {
                'family_name': family_name,
                'source_run_id': source_run_id,
                'bundle_file': Path(rel).name,
                'source_relative_path': rel,
                'source_path': meta['source_path'],
                'target_path': meta['target_path'],
                'sha256': meta['sha256'],
                'bytes': meta['bytes'],
            }
        )
    with (bundle_root / 'manifest.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    (bundle_root / 'SHA256SUMS.txt').write_text(
        '\n'.join(f"{row['sha256']}  {row['bundle_file']}" for row in rows) + '\n', encoding='utf-8'
    )
    return rows


def _write_family_readme(path: Path, *, title: str, description: str) -> None:
    path.write_text(
        f'# {title}\n\n'
        f'{description}\n\n'
        'Refresh entrypoint:\n'
        '- `scripts/refresh_cutoff_synthesis_families.py`\n',
        encoding='utf-8',
    )


def write_figure_dir_readme(path: Path, *, title: str, family_description: str) -> None:
    path.write_text(
        f'# {title}\n\n'
        f'{family_description}\n\n'
        'These are advisor-facing figure copies, not the manuscript-facing figure selection.\n'
        'The manuscript still promotes only the representative selected figure through `MANUSCRIPT_ASSET_MANIFEST.json`.\n',
        encoding='utf-8',
    )


def build_review(layout) -> None:
    out_root = layout.five_cutoff_synthesis_review_dir
    out_root.mkdir(parents=True, exist_ok=True)

    multivar_rows = list(csv.DictReader((layout.cutoff_multivariate_synthesis_dir / 'manifest.csv').open('r', encoding='utf-8')))
    reference_rows = list(csv.DictReader((layout.cutoff_reference_synthesis_dir / 'manifest.csv').open('r', encoding='utf-8')))

    md: list[str] = []
    md.append('# Five-Cutoff Synthesis Review\n\n')
    md.append('This review bundle records the cutoff-wide synthesis families promoted into the revised article repo for Stage 1 contract qualification.\n\n')
    md.append('## Family coverage\n\n')
    md.append('| Family | Cutoffs | Overlay variants | Review figure directory |\n')
    md.append('|---|---:|---:|---|\n')
    md.append(f"| `Figure 7` multivariate family | {sum(row['variant']=='primary' for row in multivar_rows)} | {sum(row['variant']=='overlay' for row in multivar_rows)} | `figures/multivariate_synthesis_by_cutoff/` |\n")
    md.append(f"| `Figure A2` reference family | {sum(row['variant']=='primary' for row in reference_rows)} | {sum(row['variant']=='overlay' for row in reference_rows)} | `figures/reference_synthesis_by_cutoff/` |\n")
    md.append('\n## Cutoff summary\n\n')
    md.append('| Cutoff | Multivariate source | Reference source |\n')
    md.append('|---|---|---|\n')
    by_cutoff_multi = {row['cutoff']: row for row in multivar_rows if row['variant'] == 'primary'}
    by_cutoff_ref = {row['cutoff']: row for row in reference_rows if row['variant'] == 'primary'}
    for cutoff in sorted(by_cutoff_multi):
        md.append(
            f"| {cutoff} | `{by_cutoff_multi[cutoff]['source_path']}` | `{by_cutoff_ref[cutoff]['source_path']}` |\n"
        )
    (out_root / 'FIVE_CUTOFF_SYNTHESIS_REVIEW.md').write_text(''.join(md), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description='Refresh cutoff-wide synthesis figure families into the revised article repo.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        '--multivar-runtime-root',
        type=Path,
        default=Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_multivar_keep_all_cutoffs_20260512'),
    )
    parser.add_argument(
        '--univar-runtime-root',
        type=Path,
        default=Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_univar_featurecov_he2_rerun_20260422'),
    )
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    multivar_runtime_root = args.multivar_runtime_root.resolve()
    univar_runtime_root = args.univar_runtime_root.resolve()
    layout = build_layout(article_root)
    layout.ensure_base_dirs()

    multivar_figure_rows: list[dict[str, str | int]] = []
    reference_figure_rows: list[dict[str, str | int]] = []

    for spec in CUTOFF_SPECS:
        multivar_output_root, univar_output_root = _source_output_roots(multivar_runtime_root, univar_runtime_root, spec)
        if not multivar_output_root.exists():
            raise FileNotFoundError(f'Missing multivariate synthesis output root: {multivar_output_root}')
        if not univar_output_root.exists():
            raise FileNotFoundError(f'Missing reference synthesis output root: {univar_output_root}')

        multivar_bundle_dir = layout.five_cutoff_main_model_synthesis_dir / spec['slug']
        reference_bundle_dir = layout.five_cutoff_reference_synthesis_dir / spec['slug']
        _write_bundle(
            multivar_bundle_dir,
            family_name='multivariate_synthesis',
            source_run_id=spec['multivar_run_id'],
            source_output_root=multivar_output_root,
            files=MULTIVAR_FILES,
        )
        _write_bundle(
            reference_bundle_dir,
            family_name='reference_synthesis',
            source_run_id=spec['univar_run_id'],
            source_output_root=univar_output_root,
            files=UNIVAR_FILES,
        )
        (multivar_bundle_dir / 'source_metadata.json').write_text(json.dumps(spec, indent=2) + '\n', encoding='utf-8')
        (reference_bundle_dir / 'source_metadata.json').write_text(json.dumps(spec, indent=2) + '\n', encoding='utf-8')

        primary_multivar = copy_file(
            multivar_output_root / 'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples.png',
            layout.cutoff_multivariate_synthesis_path(spec['slug']),
        )
        overlay_multivar = copy_file(
            multivar_output_root / 'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples_with_raw_ensembles.png',
            layout.cutoff_multivariate_synthesis_overlay_path(spec['slug']),
        )
        primary_reference = copy_file(
            univar_output_root / 'exdqlm_univar_synth_cutoff_window_posterior_samples.png',
            layout.cutoff_reference_synthesis_path(spec['slug']),
        )
        overlay_reference = copy_file(
            univar_output_root / 'exdqlm_univar_synth_cutoff_window_posterior_samples_with_raw_ensembles.png',
            layout.cutoff_reference_synthesis_overlay_path(spec['slug']),
        )

        multivar_figure_rows.extend(
            [
                {
                    'cutoff': spec['cutoff'],
                    'slug': spec['slug'],
                    'family': 'multivariate_synthesis',
                    'variant': 'primary',
                    'source_path': str(multivar_output_root / 'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples.png'),
                    'target_path': str(layout.cutoff_multivariate_synthesis_path(spec['slug']).relative_to(article_root)),
                    'sha256': primary_multivar['sha256'],
                    'bytes': primary_multivar['bytes'],
                },
                {
                    'cutoff': spec['cutoff'],
                    'slug': spec['slug'],
                    'family': 'multivariate_synthesis',
                    'variant': 'overlay',
                    'source_path': str(multivar_output_root / 'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples_with_raw_ensembles.png'),
                    'target_path': str(layout.cutoff_multivariate_synthesis_overlay_path(spec['slug']).relative_to(article_root)),
                    'sha256': overlay_multivar['sha256'],
                    'bytes': overlay_multivar['bytes'],
                },
            ]
        )
        reference_figure_rows.extend(
            [
                {
                    'cutoff': spec['cutoff'],
                    'slug': spec['slug'],
                    'family': 'reference_synthesis',
                    'variant': 'primary',
                    'source_path': str(univar_output_root / 'exdqlm_univar_synth_cutoff_window_posterior_samples.png'),
                    'target_path': str(layout.cutoff_reference_synthesis_path(spec['slug']).relative_to(article_root)),
                    'sha256': primary_reference['sha256'],
                    'bytes': primary_reference['bytes'],
                },
                {
                    'cutoff': spec['cutoff'],
                    'slug': spec['slug'],
                    'family': 'reference_synthesis',
                    'variant': 'overlay',
                    'source_path': str(univar_output_root / 'exdqlm_univar_synth_cutoff_window_posterior_samples_with_raw_ensembles.png'),
                    'target_path': str(layout.cutoff_reference_synthesis_overlay_path(spec['slug']).relative_to(article_root)),
                    'sha256': overlay_reference['sha256'],
                    'bytes': overlay_reference['bytes'],
                },
            ]
        )

    with (layout.cutoff_multivariate_synthesis_dir / 'manifest.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(multivar_figure_rows[0].keys()), lineterminator='\n')
        writer.writeheader()
        writer.writerows(multivar_figure_rows)
    with (layout.cutoff_reference_synthesis_dir / 'manifest.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(reference_figure_rows[0].keys()), lineterminator='\n')
        writer.writeheader()
        writer.writerows(reference_figure_rows)

    write_figure_dir_readme(
        layout.cutoff_multivariate_synthesis_dir / 'README.md',
        title='Multivariate Synthesis By Cutoff',
        family_description='Advisor-facing copies of the corrected Figure 7 family for all five cutoffs, including overlay companions with raw/reference ensembles.',
    )
    write_figure_dir_readme(
        layout.cutoff_reference_synthesis_dir / 'README.md',
        title='Reference Synthesis By Cutoff',
        family_description='Advisor-facing copies of the Figure A2-style reference synthesis family for all five cutoffs, including overlay companions with raw/reference ensembles.',
    )

    _write_family_readme(
        layout.five_cutoff_main_model_synthesis_dir / 'README.md',
        title='Five-Cutoff Main Model Synthesis',
        description='Frozen cutoff-by-cutoff multivariate synthesis bundles copied from the corrected `he2pubgdpc1r1` exAL main-model reruns.',
    )
    _write_family_readme(
        layout.five_cutoff_reference_synthesis_dir / 'README.md',
        title='Five-Cutoff Reference Synthesis',
        description='Frozen cutoff-by-cutoff reference synthesis bundles copied from the current publication-winning `exdqlm_univar` reruns.',
    )

    build_review(layout)
    print('Refreshed cutoff-wide synthesis figure families successfully.')


if __name__ == '__main__':
    main()
