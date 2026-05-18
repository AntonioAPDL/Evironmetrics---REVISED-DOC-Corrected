#!/usr/bin/env python3
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_RUNTIME_BINDINGS: dict[str, Any] = {
    "workflow_root": "/data/muscat_data/jaguir26/project1_ucsc_phd",
    "exal_m_t1": {
        "keep_runtime_root": "/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_multivar_keep_all_cutoffs_sharedspec_20260516",
        "univar_runtime_root": "/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_univar_all_cutoffs_sharedspec_20260516",
        "setup_support_runtime_root": "/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/exal_m_t1_setup_support_by_cutoff_v2_20260516",
        "historical_support_replay_run_root": "/data/muscat_data/jaguir26/project1_ucsc_phd_runtime/multimodel_v8_he2_exdqlm_multivar_keep_historical_support_replay_20260517/runs/multimodel_20220511_v8_he2pubgdpc1r1_exdqlm_multivar_keep_historical_support_replay",
    },
}


def binding_path(article_root: Path) -> Path:
    return article_root / "config" / "runtime_bindings.json"


def _merge_dict(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _merge_dict(base[key], value)
        else:
            base[key] = value
    return base


def load_runtime_bindings(article_root: Path) -> dict[str, Any]:
    bindings = deepcopy(DEFAULT_RUNTIME_BINDINGS)
    path = binding_path(article_root)
    if path.exists():
        override = json.loads(path.read_text(encoding="utf-8"))
        _merge_dict(bindings, override)
    return bindings


def binding_as_path(bindings: dict[str, Any], *keys: str) -> Path:
    value: Any = bindings
    for key in keys:
        value = value[key]
    return Path(str(value)).expanduser().resolve()
