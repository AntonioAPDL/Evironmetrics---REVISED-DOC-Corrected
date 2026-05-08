#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from article_asset_manifest import load_manifest, manifest_path

CUTOFF_ORDER = ['20210123', '20211112', '20211221', '20220511', '20221225']
MODEL_ORDER = ['N-U-T1', 'N-M-T0', 'N-M-T1', 'AL-U-T1', 'AL-M-T0', 'AL-M-T1', 'exAL-U-T1', 'exAL-M-T0', 'exAL-M-T1']
BENCHMARK_ROW_ORDER = ['RAW-GLOFAS', 'RAW-NWS'] + MODEL_ORDER
QUANTILE_ORDER = ['5', '20', '35', '50', '65', '80', '95']
SOURCE_ORDER = ['USGS', 'GLOFAS', 'NWS']
COMPONENT_COVARIATES = ['Precipitation', 'Soil Moisture', 'PC1']
COMPONENT_QUANTILES = ['5', '50', '95']
COMPONENT_LABELS = {'PC1': 'First GDPC factor'}
RAW_MODEL_MAP = {'RAW-GLOFAS': 'glofas_ensemble', 'RAW-NWS': 'nws_nwm_ensemble'}
RUN_SLUG_MAP = {
    '20210123': '20210123_exal_m_t1',
    '20211112': '20211112_exal_m_t1',
    '20211221': '20211221_exal_m_t1',
    '20220511': '20220511_exal_m_t1',
    '20221225': '20221225_exal_m_t1',
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as f:
        return list(csv.DictReader(f))


def fmt_num(value: str | float, digits: int) -> str:
    return f'{float(value):.{digits}f}'


def fmt_ci(row: dict[str, str], digits: int) -> str:
    return f'$[{fmt_num(row["q2_5"], digits)},\ {fmt_num(row["q97_5"], digits)}]$'


def build_benchmark_rows(article_root: Path, table_cfg: dict) -> tuple[list[str], list[str], list[dict[str, str]]]:
    manifest_rows = read_csv(article_root / table_cfg['sources']['bayesian_manifest_csv'])
    bayes = {(row['manuscript_label'], row['cutoff']): row for row in manifest_rows}
    raw_rows: dict[tuple[str, str], str] = {}
    five_root = article_root / table_cfg['sources']['five_run_source_root']
    for cutoff in CUTOFF_ORDER:
        slug = RUN_SLUG_MAP[cutoff]
        crps_rows = read_csv(five_root / slug / 'crps_forecast_summary.csv')
        by_model = {row['model_id']: row for row in crps_rows}
        for raw_label, model_id in RAW_MODEL_MAP.items():
            raw_rows[(raw_label, cutoff)] = by_model[model_id]['mean_crps']

    values_by_cutoff: dict[str, dict[str, float]] = {cutoff: {} for cutoff in CUTOFF_ORDER}
    for cutoff in CUTOFF_ORDER:
        for raw_label in RAW_MODEL_MAP:
            values_by_cutoff[cutoff][raw_label] = float(raw_rows[(raw_label, cutoff)])
        for label in MODEL_ORDER:
            values_by_cutoff[cutoff][label] = float(bayes[(label, cutoff)]['crps_exact'])

    best_by_cutoff = {cutoff: min(vals.values()) for cutoff, vals in values_by_cutoff.items()}

    raw_lines: list[str] = []
    bayesian_lines: list[str] = []
    manifest_out: list[dict[str, str]] = []
    for row_label in ['RAW-GLOFAS', 'RAW-NWS']:
        parts = [row_label]
        for cutoff in CUTOFF_ORDER:
            value = values_by_cutoff[cutoff][row_label]
            rendered = f'{value:.4f}'
            if abs(value - best_by_cutoff[cutoff]) < 1e-12:
                rendered = f'\\textbf{{{rendered}}}'
            parts.append(rendered)
        raw_lines.append(' & '.join(parts) + ' \\\\')
        manifest_out.append({
            'table_label': 'tab:benchmark_crps_models',
            'row_label': row_label,
            'source_class': table_cfg['source_class'],
            'source_note': table_cfg['note'],
        })
    for row_label in MODEL_ORDER:
        parts = [row_label]
        for cutoff in CUTOFF_ORDER:
            value = values_by_cutoff[cutoff][row_label]
            rendered = f'{value:.4f}'
            if abs(value - best_by_cutoff[cutoff]) < 1e-12:
                rendered = f'\\textbf{{{rendered}}}'
            parts.append(rendered)
        bayesian_lines.append(' & '.join(parts) + ' \\\\')
        manifest_out.append({
            'table_label': 'tab:benchmark_crps_models',
            'row_label': row_label,
            'source_class': table_cfg['source_class'],
            'source_note': table_cfg['note'],
        })
    return raw_lines, bayesian_lines, manifest_out


def build_component_rows(article_root: Path, table_cfg: dict) -> tuple[list[str], list[dict[str, str]]]:
    rows = read_csv(article_root / table_cfg['sources']['covariate_effects_csv'])
    lookup = {(row['covariate'], row['quantile']): row for row in rows}
    q_label = {'5': '5th', '50': '50th', '95': '95th'}
    lines: list[str] = []
    manifest_out: list[dict[str, str]] = []
    for cov in COMPONENT_COVARIATES:
        display = COMPONENT_LABELS.get(cov, cov)
        for idx, q in enumerate(COMPONENT_QUANTILES):
            row = lookup[(cov, q)]
            prefix = f'\\multirow{{3}}{{*}}{{{display}}}' if idx == 0 else ''
            connector = '&' if idx > 0 else '  &'
            lines.append(f'{prefix}{connector} {q_label[q]} & {fmt_num(row["center"], 3)} & {fmt_ci(row, 3)} \\\\')
            manifest_out.append({'table_label': 'tab:components_23_31', 'row_label': f'{cov}_{q}', 'source_class': table_cfg['source_class'], 'source_note': table_cfg['note']})
        if cov != COMPONENT_COVARIATES[-1]:
            lines.append('\\midrule')
    return lines, manifest_out


def build_source_summary_rows(article_root: Path, table_cfg: dict, table_label: str, digits: int) -> tuple[list[str], list[dict[str, str]]]:
    source_key = 'gamma_summary_csv' if table_label == 'tab:gamma_sigma_intervals1' else 'sigma_summary_csv'
    rows = read_csv(article_root / table_cfg['sources'][source_key])
    lookup = {(row['quantile'], row['source']): row for row in rows}
    q_label = {'5': '05th', '20': '20th', '35': '35th', '50': '50th', '65': '65th', '80': '80th', '95': '95th'}
    lines: list[str] = []
    manifest_out: list[dict[str, str]] = []
    for q in QUANTILE_ORDER:
        cells = [q_label[q]]
        for source in SOURCE_ORDER:
            row = lookup[(q, source)]
            cells.append(fmt_num(row['center'], digits))
            cells.append(fmt_ci(row, digits))
            manifest_out.append({'table_label': table_label, 'row_label': f'{q}_{source}', 'source_class': table_cfg['source_class'], 'source_note': table_cfg['note']})
        lines.append(' & '.join(cells) + ' \\\\')
    return lines, manifest_out


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(lines) + '\n')


def main() -> None:
    parser = argparse.ArgumentParser(description='Build generated TeX table includes for the revised article.')
    parser.add_argument('--article-root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    manifest = load_manifest(article_root)
    out_root = article_root / 'generated' / 'article_table_includes'
    out_root.mkdir(parents=True, exist_ok=True)

    manifest_rows: list[dict[str, str]] = []

    benchmark_raw_lines, benchmark_bayesian_lines, rows = build_benchmark_rows(article_root, manifest['tables']['tab:benchmark_crps_models'])
    manifest_rows.extend(rows)
    write_lines(out_root / 'table_benchmark_crps_rows.tex', benchmark_raw_lines)
    write_lines(out_root / 'table_benchmark_bayesian_rows.tex', benchmark_bayesian_lines)

    component_lines, rows = build_component_rows(article_root, manifest['tables']['tab:components_23_31'])
    manifest_rows.extend(rows)
    write_lines(out_root / 'table_components_23_31_rows.tex', component_lines)

    gamma_lines, rows = build_source_summary_rows(article_root, manifest['tables']['tab:gamma_sigma_intervals1'], 'tab:gamma_sigma_intervals1', 3)
    manifest_rows.extend(rows)
    write_lines(out_root / 'table_gamma_rows.tex', gamma_lines)

    sigma_lines, rows = build_source_summary_rows(article_root, manifest['tables']['tab:gamma_sigma_intervals2'], 'tab:gamma_sigma_intervals2', 5)
    manifest_rows.extend(rows)
    write_lines(out_root / 'table_sigma_rows.tex', sigma_lines)

    with (out_root / 'manifest.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['table_label', 'row_label', 'source_class', 'source_note'])
        writer.writeheader()
        writer.writerows(manifest_rows)

    metadata = {
        'manifest_path': str(manifest_path(article_root)),
        'outputs': {
            'tab:benchmark_crps_models': 'generated/article_table_includes/table_benchmark_crps_rows.tex',
            'tab:benchmark_crps_models_bayesian': 'generated/article_table_includes/table_benchmark_bayesian_rows.tex',
            'tab:components_23_31': 'generated/article_table_includes/table_components_23_31_rows.tex',
            'tab:gamma_sigma_intervals1': 'generated/article_table_includes/table_gamma_rows.tex',
            'tab:gamma_sigma_intervals2': 'generated/article_table_includes/table_sigma_rows.tex'
        }
    }
    (out_root / 'build_metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    (out_root / 'README.md').write_text(
        '# Article Table Includes\n\n'
        'These TeX row snippets are generated from the article-side frozen data sources named in `ARTICLE_GENERATED_ASSET_MANIFEST.json`.\n\n'
        'Refresh path:\n'
        '- `scripts/build_generated_table_includes.py`\n\n'
        'The manuscript uses `\\input{}` to consume these files directly.\n'
    )
    print(f'Built generated table includes in {out_root}')


if __name__ == '__main__':
    main()
