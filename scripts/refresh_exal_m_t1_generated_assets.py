#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
from pathlib import Path

from article_repo_layout import build_layout

FIVE_RUN_SPECS = [
    {
        'slug': '20210123_exal_m_t1',
        'cutoff': '2021-01-23',
        'published_crps': '0.1569',
        'run_id': 'multimodel_20210123_v8_eps360cf1_exdqlm_multivar_keep_featurecov_cf1',
    },
    {
        'slug': '20211112_exal_m_t1',
        'cutoff': '2021-11-12',
        'published_crps': '0.0284',
        'run_id': 'multimodel_20211112_v8_eps180cf1_exdqlm_multivar_keep_featurecov_cf1',
    },
    {
        'slug': '20211221_exal_m_t1',
        'cutoff': '2021-12-21',
        'published_crps': '0.2369',
        'run_id': 'multimodel_20211221_v8_eps1cf1_exdqlm_multivar_keep_featurecov_cf1',
    },
    {
        'slug': '20220511_exal_m_t1',
        'cutoff': '2022-05-11',
        'published_crps': '0.0210',
        'run_id': 'multimodel_20220511_v8_eps180cf1_exdqlm_multivar_keep_featurecov_cf1',
    },
    {
        'slug': '20221225_exal_m_t1',
        'cutoff': '2022-12-25',
        'published_crps': '0.4375',
        'run_id': 'multimodel_20221225_v8_exalm_t1_discount_grid_exact_v1_set09_exdqlm_multivar_keep',
    },
]

REPRESENTATIVE_FILES = [
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples.pdf',
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples.png',
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples_with_raw_ensembles.pdf',
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples_with_raw_ensembles.png',
    'exdqlm_multivar_synth_keep_cutoff_window_quantiles.csv',
    'exdqlm_multivar_synth_keep_cutoff_window_sample_subset.csv',
    'figure_manifest.csv',
    'publication_figure_manifest.csv',
    'publication_style_used.yaml',
    'tables/covariate_effects_summary.csv',
    'tables/covariate_effects_summary.tex',
    'tables/crps_forecast_per_time.csv',
    'tables/crps_forecast_summary.csv',
    'tables/gamma_summary.csv',
    'tables/gamma_summary.tex',
    'tables/posterior_table_exports_manifest.csv',
    'tables/posterior_table_exports_README.md',
    'tables/sigma_summary.csv',
    'tables/sigma_summary.tex',
]

ALIAS_FIGURES = {
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples.png': 'representative_synthesis_multivariate.png',
    'exdqlm_multivar_synth_keep_cutoff_window_posterior_samples_with_raw_ensembles.png': 'representative_synthesis_multivariate_with_reference_ensembles.png',
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_file(src: Path, dst: Path) -> str:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return sha256(dst)


def read_mean_crps(path: Path) -> str:
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    target = next((r for r in rows if r.get('model_id') == 'exdqlm_multivar_synth_keep'), rows[0])
    return target['mean_crps']


def refresh_five_run_sources(layout, runtime_root: Path) -> None:
    bundle_root = layout.five_cutoff_crps_validation_dir
    bundle_root.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    sums = []

    for spec in FIVE_RUN_SPECS:
        run_root = runtime_root / spec['slug'] / 'runs' / spec['run_id']
        output_root = run_root / 'post' / 'outputs' / spec['run_id']
        target_dir = bundle_root / spec['slug']
        target_dir.mkdir(parents=True, exist_ok=True)

        src_summary = run_root / 'report' / 'summary.json'
        src_compare = run_root / 'validate' / 'compare_report.json'
        src_crps = output_root / 'tables' / 'crps_forecast_summary.csv'

        out_summary = target_dir / 'summary.json'
        out_compare = target_dir / 'compare_report.json'
        out_crps = target_dir / 'crps_forecast_summary.csv'

        for src, dst in ((src_summary, out_summary), (src_compare, out_compare), (src_crps, out_crps)):
            digest = copy_file(src, dst)
            sums.append(f'{digest}  {spec["slug"]}/{dst.name}')

        manifest_rows.append([
            spec['slug'],
            spec['cutoff'],
            spec['run_id'],
            spec['published_crps'],
            read_mean_crps(out_crps),
            str(run_root),
            str(src_summary),
            str(src_compare),
            str(src_crps),
            str(out_summary.relative_to(layout.root)),
            str(out_compare.relative_to(layout.root)),
            str(out_crps.relative_to(layout.root)),
        ])

    (bundle_root / 'README.md').write_text(
        '# Five-Cutoff CRPS Validation Sources\n\n'
        'This artifact bundle freezes the five verified publication `exAL-M-T1` run roots used by the revised article benchmark table.\n\n'
        'Refresh script:\n'
        '- `scripts/refresh_exal_m_t1_generated_assets.py`\n\n'
        'For each cutoff, the local freeze contains:\n'
        '- `summary.json`\n'
        '- `compare_report.json`\n'
        '- `crps_forecast_summary.csv`\n\n'
        'These files are copied from the verified publication replay representative runtime roots.\n'
    )

    with (bundle_root / 'manifest.csv').open('w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([
            'slug', 'cutoff', 'run_id', 'published_crps', 'replay_mean_crps', 'runtime_run_root',
            'source_summary_json', 'source_compare_report', 'source_crps_summary',
            'local_summary_json', 'local_compare_report', 'local_crps_summary'
        ])
        writer.writerows(manifest_rows)
    (bundle_root / 'SHA256SUMS.txt').write_text('\n'.join(sorted(sums)) + '\n')


def refresh_representative_bundle(layout, runtime_root: Path) -> None:
    spec = next(s for s in FIVE_RUN_SPECS if s['slug'] == '20221225_exal_m_t1')
    run_root = runtime_root / spec['slug'] / 'runs' / spec['run_id']
    output_root = run_root / 'post' / 'outputs' / spec['run_id']
    bundle_root = layout.representative_selected_model_dir
    bundle_root.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    sums = []
    for rel in REPRESENTATIVE_FILES:
        src = output_root / rel
        dst = bundle_root / Path(rel).name
        digest = copy_file(src, dst)
        sums.append(f'{digest}  {dst.name}')
        manifest_rows.append([rel, dst.name, str(src), str(dst.relative_to(layout.root)), digest])

    for src_name, alias_name in ALIAS_FIGURES.items():
        src = bundle_root / src_name
        dst = bundle_root / alias_name
        shutil.copy2(src, dst)
        sums.append(f'{sha256(dst)}  {alias_name}')
        manifest_rows.append([src_name, alias_name, str(src), str(dst.relative_to(layout.root)), sha256(dst)])

    for src, dst_name in ((run_root / 'report' / 'summary.json', 'summary.json'), (run_root / 'validate' / 'compare_report.json', 'compare_report.json')):
        digest = copy_file(src, bundle_root / dst_name)
        sums.append(f'{digest}  {dst_name}')
        manifest_rows.append([str(src.relative_to(run_root)), dst_name, str(src), str((bundle_root / dst_name).relative_to(layout.root)), digest])

    metadata = {
        'cutoff': spec['cutoff'],
        'run_id': spec['run_id'],
        'runtime_run_root': str(run_root),
        'runtime_output_root': str(output_root),
        'published_crps': spec['published_crps'],
        'replay_mean_crps': read_mean_crps(bundle_root / 'crps_forecast_summary.csv'),
    }
    (bundle_root / 'bundle_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')

    (bundle_root / 'README.md').write_text(
        '# Representative Selected Model: 2022-12-25\n\n'
        'This artifact bundle freezes the verified representative `2022-12-25 exAL-M-T1` outputs used by the revised article.\n\n'
        'Refresh script:\n'
        '- `scripts/refresh_exal_m_t1_generated_assets.py`\n\n'
        'Included content:\n'
        '- selected synthesis figures\n'
        '- quantile and sample exports\n'
        '- CRPS summaries\n'
        '- posterior table exports\n'
        '- figure manifests\n'
        '- report and validation summaries\n'
    )
    with (bundle_root / 'manifest.csv').open('w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['source_relative_path', 'local_filename', 'source_absolute_path', 'local_bundle_path', 'sha256'])
        writer.writerows(manifest_rows)
    (bundle_root / 'SHA256SUMS.txt').write_text('\n'.join(sorted(sums)) + '\n')


def main() -> None:
    parser = argparse.ArgumentParser(description='Refresh article-side exAL-M-T1 generated asset bundles.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--runtime-root', type=Path, default=Path('/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_publication_replay_representatives_20260506'))
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    runtime_root = args.runtime_root.resolve()
    layout = build_layout(article_root)
    layout.ensure_base_dirs()
    refresh_five_run_sources(layout, runtime_root)
    refresh_representative_bundle(layout, runtime_root)
    print('Refreshed exAL-M-T1 generated asset bundles successfully.')


if __name__ == '__main__':
    main()
