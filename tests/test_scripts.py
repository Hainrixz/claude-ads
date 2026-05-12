"""Script smoke tests.

Each ``scripts/*.py`` that exposes a CLI (``if __name__ == "__main__":``)
must respond to ``--help`` without error. This catches:

* Broken imports (missing dependency in requirements.txt).
* Missing argparse setup.
* Scripts that crash at import time.

We skip ``scripts/lib/*`` since those are library modules, not CLIs.
We also skip the ``--help`` smoke test when a script's runtime dependency
is not installed (e.g. Playwright on a bare machine). The dependency map
below mirrors what each script imports at module load.
"""
from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

from tests._helpers import REPO_ROOT

SCRIPTS_DIR = REPO_ROOT / "scripts"

# Map each CLI script to its runtime dependencies (importable module names).
# If any are missing, the --help smoke is skipped for that script.
SCRIPT_DEPS: dict[str, tuple[str, ...]] = {
    "analyze_landing.py": ("playwright", "requests"),
    "capture_screenshot.py": ("playwright",),
    "fetch_page.py": ("requests",),
    "generate_image.py": ("PIL",),
    "generate_report.py": ("reportlab", "matplotlib"),
}

# Some scripts use PEP 604 union syntax (X | Y) which requires Python 3.10+.
# CI runs 3.12 so these pass; document the minimum so older local envs skip.
SCRIPT_MIN_PYTHON: dict[str, tuple[int, int]] = {
    "generate_image.py": (3, 10),
}


def _has_cli_entry(script_path: Path) -> bool:
    """Return True if the script has an ``if __name__ == "__main__":`` block."""
    try:
        tree = ast.parse(script_path.read_text(encoding="utf-8"))
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and isinstance(node.test, ast.Compare):
            left = node.test.left
            if isinstance(left, ast.Name) and left.id == "__name__":
                return True
    return False


CLI_SCRIPTS = sorted(
    p for p in (
        list(SCRIPTS_DIR.glob("*.py"))
        + list((SCRIPTS_DIR / "api").glob("*.py"))
    )
    if p.name != "__init__.py" and _has_cli_entry(p)
)


@pytest.mark.parametrize("script_path", CLI_SCRIPTS, ids=lambda p: p.name)
def test_script_has_module_docstring(script_path: Path) -> None:
    tree = ast.parse(script_path.read_text(encoding="utf-8"))
    doc = ast.get_docstring(tree)
    assert doc, f"{script_path.name}: missing module docstring (project rule)"


@pytest.mark.parametrize("script_path", CLI_SCRIPTS, ids=lambda p: p.name)
def test_script_help_smoke(script_path: Path) -> None:
    """Run ``python <script> --help`` and assert it exits cleanly.

    Skipped when a runtime dependency is missing — that's an environment
    issue, not a regression in the script itself.
    """
    for dep in SCRIPT_DEPS.get(script_path.name, ()):
        if importlib.util.find_spec(dep) is None:
            pytest.skip(f"{script_path.name}: required module {dep!r} not installed")

    min_py = SCRIPT_MIN_PYTHON.get(script_path.name)
    if min_py and sys.version_info[:2] < min_py:
        pytest.skip(
            f"{script_path.name}: requires Python {min_py[0]}.{min_py[1]}+, "
            f"running on {sys.version_info.major}.{sys.version_info.minor}"
        )

    proc = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, (
        f"{script_path.name}: --help exited {proc.returncode}\n"
        f"stdout: {proc.stdout[:500]}\nstderr: {proc.stderr[:500]}"
    )
    # The help output should mention the script's purpose or usage.
    assert proc.stdout, f"{script_path.name}: --help produced no output"
