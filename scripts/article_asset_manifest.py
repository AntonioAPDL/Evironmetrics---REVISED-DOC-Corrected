#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MANIFEST_FILENAME = 'ARTICLE_GENERATED_ASSET_MANIFEST.json'


def load_manifest(article_root: Path) -> dict[str, Any]:
    path = article_root / MANIFEST_FILENAME
    return json.loads(path.read_text())


def manifest_path(article_root: Path) -> Path:
    return article_root / MANIFEST_FILENAME
