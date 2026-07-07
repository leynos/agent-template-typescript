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


def test_spelling_gate_files_present_by_default(
    tmp_path: Path, copier: CopierFixture
) -> None:
    """Default render ships the en-GB-oxendict spelling gate."""
    project = copier.copy(
        tmp_path,
        project_name="spelling-on",
        project_title="Spelling On",
        project_description="A test project",
        github_username="testuser",
    )
    assert (project / "typos.toml").exists(), "typos.toml should exist"
    assert (
        project / "scripts" / "generate_typos_config.py"
    ).exists(), "generator script should exist"
    assert (
        project / "docs" / "spelling-gate.md"
    ).exists(), "spelling gate docs should exist"
    makefile = (project / "Makefile").read_text()
    assert "TYPOS_VERSION" in makefile, "Makefile should pin the typos version"
    assert (
        "generate_typos_config.py --check" in makefile
    ), "Makefile should run the drift check"
    assert (
        "--config typos.toml" in makefile
    ), "Makefile should run typos with the generated config"


def test_spelling_gate_disabled_leaves_no_trace(
    tmp_path: Path, copier: CopierFixture
) -> None:
    """Disabling the toggle removes every trace of the spelling gate."""
    project = copier.copy(
        tmp_path,
        project_name="spelling-off",
        project_title="Spelling Off",
        project_description="A test project",
        github_username="testuser",
        en_gb_oxendict=False,
    )
    assert not (project / "typos.toml").exists(), "typos.toml should be absent"
    assert not (project / "scripts").exists(), "scripts/ should be absent"
    assert not (project / "docs").exists(), "docs/ should be absent"
    makefile = (project / "Makefile").read_text()
    assert "typos" not in makefile, "Makefile should not mention typos"
    assert "TYPOS_VERSION" not in makefile, "Makefile should not pin typos"


def test_spelling_config_matches_generator_output(
    tmp_path: Path, copier: CopierFixture
) -> None:
    """The rendered typos.toml passes the generator's --check drift gate."""
    project = copier.copy(
        tmp_path,
        project_name="spelling-drift",
        project_title="Spelling Drift",
        project_description="A test project",
        github_username="testuser",
    )
    project.run("python3 scripts/generate_typos_config.py --check")


def test_spelling_config_parses_with_expected_entry_count(
    tmp_path: Path, copier: CopierFixture
) -> None:
    """The rendered typos.toml parses as TOML with no duplicate keys.

    ``tomllib`` raises ``TOMLDecodeError`` on duplicate keys, so parsing
    guards against two stem/suffix combinations (or an extra accepted
    word) colliding into the same ``extend-words`` entry. The exact entry
    count additionally documents that every stem inflection and accepted
    word is present.
    """
    import importlib.util
    import tomllib

    project = copier.copy(
        tmp_path,
        project_name="spelling-parse",
        project_title="Spelling Parse",
        project_description="A test project",
        github_username="testuser",
    )
    script = project / "scripts" / "generate_typos_config.py"
    spec = importlib.util.spec_from_file_location("generate_typos_config", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    committed = (project / "typos.toml").read_text(encoding="utf-8")
    parsed = tomllib.loads(committed)
    assert parsed["default"]["locale"] == "en-gb"
    extend_words = parsed["default"]["extend-words"]
    expected = len(module.EXTRA_ACCEPTED_WORDS) + 2 * len(module.STEMS) * len(
        module.SUFFIX_PAIRS
    )
    assert len(extend_words) == expected
    assert committed == module.render_config()


def test_makefile_markdownlint_runs_spelling_gate(
    tmp_path: Path, copier: CopierFixture
) -> None:
    """Generated project passes make markdownlint including the typos gate."""
    project = copier.copy(
        tmp_path,
        project_name="spelling-make",
        project_title="Spelling Make",
        project_description="A test project",
        github_username="testuser",
    )
    project.run("make markdownlint")
