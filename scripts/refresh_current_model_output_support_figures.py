#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from article_repo_layout import build_layout

MULTIVAR_SPEC = {
    "slug": "20220511_exal_m_t1",
    "cutoff": "2022-05-11",
    "forecast_start": "2022-05-12",
    "run_id": "multimodel_20220511_v8_he2pubgdpc1r1_exdqlm_multivar_keep",
}

UNIVAR_SPEC = {
    "cutoff": "2022-12-25",
    "run_id": "multimodel_20221225_v8_univar_featurecov_he2_v1_exdqlm_univar",
    "source_png": "exdqlm_univar_synth_cutoff_window_posterior_samples.png",
}

RENAMES = {
    "All_exal_2012-2016_DISC.png": "historical_summary_dry_period.png",
    "All_exal_2017-2019_DISC.png": "historical_summary_wet_period.png",
    "All_exal_2017-2019_DISC_fullrange.png": "historical_summary_wet_period_fullrange.png",
    "80_component_1991_2022.png": "historical_component_80month.png",
    "posterior_samples_counter_valid.png": "reference_synthesis_univariate.png",
}

HISTORICAL_FIGURES = [
    ("fig:dry_quantile", "historical_summary_dry_period.png", "Dry-period historical summary"),
    ("fig:rainy_quantile", "historical_summary_wet_period.png", "Rainy-period historical summary"),
    ("companion:rainy_quantile_fullrange", "historical_summary_wet_period_fullrange.png", "Wet-period historical summary (0-20 companion range)"),
    ("fig:80_components", "historical_component_80month.png", "Long-cycle component summary"),
]

APPENDIX_FIGURE = ("fig:synth2", "reference_synthesis_univariate.png", "Historical-only reference synthesis")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd: list[str]) -> None:
    print("+", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def apply_renames(figures_dir: Path) -> None:
    for src_name, dst_name in RENAMES.items():
        src = figures_dir / src_name
        dst = figures_dir / dst_name
        if src.exists():
            if dst.exists():
                dst.unlink()
            shutil.move(src, dst)


def write_bundle(bundle_root: Path, multivar_run_root: Path, univar_output_root: Path) -> None:
    figures_dir = bundle_root / "figures"
    rows: list[list[str]] = []
    sums: list[str] = []

    for label, filename, role in HISTORICAL_FIGURES:
        path = figures_dir / filename
        digest = sha256(path)
        rows.append([
            label,
            filename,
            role,
            "rendered_from_current_multivar_run",
            str(multivar_run_root),
            str(path.relative_to(bundle_root.parent.parent)),
            digest,
        ])
        sums.append(f"{digest}  figures/{filename}")

    label, filename, role = APPENDIX_FIGURE
    path = figures_dir / filename
    digest = sha256(path)
    rows.append([
        label,
        filename,
        role,
        "copied_from_current_univar_output",
        str(univar_output_root / UNIVAR_SPEC["source_png"]),
        str(path.relative_to(bundle_root.parent.parent)),
        digest,
    ])
    sums.append(f"{digest}  figures/{filename}")

    metadata = {
        "multivar_source": {
            "slug": MULTIVAR_SPEC["slug"],
            "cutoff": MULTIVAR_SPEC["cutoff"],
            "run_id": MULTIVAR_SPEC["run_id"],
            "runtime_run_root": str(multivar_run_root),
        },
        "univar_source": {
            "cutoff": UNIVAR_SPEC["cutoff"],
            "run_id": UNIVAR_SPEC["run_id"],
            "output_root": str(univar_output_root),
            "copied_png": UNIVAR_SPEC["source_png"],
        },
    }
    (bundle_root / "bundle_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    (bundle_root / "README.md").write_text(
        "# Historical Support From Current Models\n\n"
        "This article-side artifact bundle regenerates the historical-support manuscript figures from current model outputs.\n\n"
        "Sources:\n"
        f"- Historical multivariate support figures: `{multivar_run_root}`\n"
        f"- Historical-only univariate reference figure: `{univar_output_root / UNIVAR_SPEC['source_png']}`\n\n"
        "Refresh entrypoint:\n"
        "- `scripts/refresh_current_model_output_support_figures.py`\n"
    )

    with (bundle_root / "manifest.csv").open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow([
            "label",
            "filename",
            "role",
            "generation_mode",
            "source_path",
            "local_bundle_path",
            "sha256",
        ])
        writer.writerows(rows)

    (bundle_root / "SHA256SUMS.txt").write_text("\n".join(sorted(sums)) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh current-model support figures for the revised article.")
    parser.add_argument("--article-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--workflow-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--multivar-runtime-root",
        type=Path,
        default=Path("/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_multivar_keep_all_cutoffs_20260512"),
    )
    parser.add_argument(
        "--univar-runtime-root",
        type=Path,
        default=Path("/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_univar_featurecov_he2_rerun_20260422"),
    )
    args = parser.parse_args()

    article_root = args.article_root.resolve()
    workflow_root = args.workflow_root.resolve()
    multivar_runtime_root = args.multivar_runtime_root.resolve()
    univar_runtime_root = args.univar_runtime_root.resolve()

    layout = build_layout(article_root)
    layout.ensure_base_dirs()
    bundle_root = layout.historical_support_dir
    figures_dir = bundle_root / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    multivar_run_root = multivar_runtime_root / "runs" / MULTIVAR_SPEC["run_id"]
    univar_output_root = (
        univar_runtime_root / "runs" / UNIVAR_SPEC["run_id"] / "post" / "outputs" / UNIVAR_SPEC["run_id"]
    )
    univar_png = univar_output_root / UNIVAR_SPEC["source_png"]

    if not multivar_run_root.exists():
        raise FileNotFoundError(f"Missing multivariate source run: {multivar_run_root}")
    if not univar_png.exists():
        raise FileNotFoundError(f"Missing univariate source PNG: {univar_png}")

    run([
        "Rscript",
        str(article_root / "scripts" / "render_current_model_output_support_figures.R"),
        "--workflow-root", str(workflow_root),
        "--run-root", str(multivar_run_root),
        "--output-dir", str(figures_dir),
        "--cutoff-date", MULTIVAR_SPEC["cutoff"],
        "--forecast-start-date", MULTIVAR_SPEC["forecast_start"],
    ])

    shutil.copy2(univar_png, figures_dir / "posterior_samples_counter_valid.png")
    apply_renames(figures_dir)
    write_bundle(bundle_root, multivar_run_root, univar_output_root)
    print("Refreshed current-model output support figures successfully.")


if __name__ == "__main__":
    main()
