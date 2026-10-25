# Portions Copyright (c) 2026 Enrique Rocha (@soyenriquerocha) - see LICENSE for original authors
# SPDX-License-Identifier: MIT
# id: er-fd4fa55b
"""Pytest configuration — ensure the repo root is importable for ``tests._helpers``."""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
