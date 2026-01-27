"""Template rendering and validation tests.

Validates that the Copier template renders correctly with default values
and that the generated project passes build, typecheck, lint, test, and
format-check workflows.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_copier.plugin import CopierFixture


def test_template_renders(tmp_path: Path, copier: CopierFixture) -> None:
    """Template renders with default values."""
    project = copier.copy(
        tmp_path,
        project_name="example-project",
        project_title="Example Project",
        project_description="A test project",
        github_username="testuser",
    )
    assert (project / "package.json").exists(), "package.json should exist"
    assert (project / "tsconfig.json").exists(), "tsconfig.json should exist"
    assert (project / "biome.jsonc").exists(), "biome.jsonc should exist"
    assert (project / "Makefile").exists(), "Makefile should exist"
    assert (project / "src" / "index.ts").exists(), "src/index.ts should exist"
    assert (
        project / "tests" / "index.test.ts"
    ).exists(), "tests/index.test.ts should exist"


@pytest.mark.parametrize(
    ("project_name", "make_target"),
    [
        ("build-example", "build"),
        ("typecheck-example", "typecheck"),
        ("lint-example", "lint"),
        ("test-example", "test"),
        ("format-example", "check-fmt"),
    ],
    ids=["build", "typecheck", "lint", "test", "check-fmt"],
)
def test_template_make_target(
    tmp_path: Path,
    copier: CopierFixture,
    project_name: str,
    make_target: str,
) -> None:
    """Generated project passes make target."""
    project = copier.copy(
        tmp_path,
        project_name=project_name,
        project_title=project_name.replace("-", " ").title(),
        project_description="A test project",
        github_username="testuser",
    )
    project.run(f"make {make_target}")


def test_package_json_has_correct_name(tmp_path: Path, copier: CopierFixture) -> None:
    """Generated package.json has the correct project name."""
    project = copier.copy(
        tmp_path,
        project_name="my-cool-project",
        project_title="My Cool Project",
        project_description="A cool project",
        github_username="cooluser",
    )
    package_json = (project / "package.json").read_text()
    assert (
        '"name": "my-cool-project"' in package_json
    ), "package.json should contain the correct project name"
