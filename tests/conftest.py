"""Pytest fixtures for Copier template testing.

Provides fixtures that configure pytest-copier to locate and copy only the
relevant template files (copier.yml and template directory) during test runs.

Examples
--------
These fixtures are automatically discovered by pytest-copier. Tests can use
the ``copier`` fixture (of type ``pytest_copier.CopierFixture``) to generate
projects::

    def test_template_renders(tmp_path: Path, copier: CopierFixture) -> None:
        project = copier.copy(
            tmp_path,
            project_name="example",
            project_title="Example",
        )
        assert (project / "package.json").exists()
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def copier_template_paths() -> list[str]:
    """Specify which paths to copy to the test template directory.

    This prevents copying .git and other non-template files.

    Returns
    -------
    list[str]
        List of paths to include when copying the template for testing.
    """
    return ["copier.yml", "template"]


@pytest.fixture(scope="session")
def copier_template_root() -> Path:
    """Return the root directory of the Copier template.

    Returns
    -------
    Path
        Absolute path to the template root directory.
    """
    return Path(__file__).parents[1]
