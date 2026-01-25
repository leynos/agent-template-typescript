"""Pytest fixtures for Copier template testing.

Provides fixtures that configure pytest-copier to locate and copy only the
relevant template files (copier.yml and template directory) during test runs.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def copier_template_paths() -> list[str]:
    """Specify which paths to copy to the test template directory.

    This prevents copying .git and other non-template files.
    """
    return ["copier.yml", "template"]


@pytest.fixture(scope="session")
def copier_template_root() -> Path:
    """Root directory of the copier template."""
    return Path(__file__).parents[1]
