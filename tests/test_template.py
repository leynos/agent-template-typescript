from __future__ import annotations

from pathlib import Path

from pytest_copier.plugin import CopierFixture


TEMPLATE_PATH = Path(__file__).parents[1]


def test_template_renders(tmp_path: Path, copier: CopierFixture) -> None:
    """Template renders with default values."""
    project = copier.copy(
        tmp_path,
        project_name="example-project",
        project_title="Example Project",
        project_description="A test project",
        github_username="testuser",
    )
    assert (project / "package.json").exists()
    assert (project / "tsconfig.json").exists()
    assert (project / "biome.jsonc").exists()
    assert (project / "Makefile").exists()
    assert (project / "src" / "index.ts").exists()
    assert (project / "tests" / "index.test.ts").exists()


def test_template_builds(tmp_path: Path, copier: CopierFixture) -> None:
    """Generated project installs dependencies."""
    project = copier.copy(
        tmp_path,
        project_name="build-example",
        project_title="Build Example",
        project_description="A test project",
        github_username="testuser",
    )
    project.run("make build")


def test_template_typechecks(tmp_path: Path, copier: CopierFixture) -> None:
    """Generated project passes type checking."""
    project = copier.copy(
        tmp_path,
        project_name="typecheck-example",
        project_title="Typecheck Example",
        project_description="A test project",
        github_username="testuser",
    )
    project.run("make typecheck")


def test_template_lints(tmp_path: Path, copier: CopierFixture) -> None:
    """Generated project passes linting."""
    project = copier.copy(
        tmp_path,
        project_name="lint-example",
        project_title="Lint Example",
        project_description="A test project",
        github_username="testuser",
    )
    project.run("make lint")


def test_template_tests(tmp_path: Path, copier: CopierFixture) -> None:
    """Generated project tests pass."""
    project = copier.copy(
        tmp_path,
        project_name="test-example",
        project_title="Test Example",
        project_description="A test project",
        github_username="testuser",
    )
    project.run("make test")


def test_template_format_check(tmp_path: Path, copier: CopierFixture) -> None:
    """Generated project passes format checking."""
    project = copier.copy(
        tmp_path,
        project_name="format-example",
        project_title="Format Example",
        project_description="A test project",
        github_username="testuser",
    )
    project.run("make check-fmt")


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
    assert '"name": "my-cool-project"' in package_json
