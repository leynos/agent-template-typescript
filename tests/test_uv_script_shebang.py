"""Tests for the uv script shebang convention.

Standalone Python scripts that declare a PEP 723 inline metadata block must
use ``#!/usr/bin/env -S uv run --script`` so ``uv`` installs the declared
dependencies before execution. The superficially similar
``#!/usr/bin/env -S uv run python`` shebang runs the interpreter directly and
skips the metadata block entirely, so the script fails at import time when a
dependency is not already installed.
"""

from __future__ import annotations

import pathlib
import shutil
import stat
import subprocess  # noqa: S404 - runs the pinned, trusted uv binary.
import textwrap

import pytest

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
BROKEN_SHEBANG = "#!/usr/bin/env -S uv run python"
CORRECT_SHEBANG = "#!/usr/bin/env -S uv run --script"
PEP723_MARKER = "# /// script"


def _scripts_with_pep723_metadata() -> list[pathlib.Path]:
    """Return every tracked, executable script with a PEP 723 metadata block.

    Only files whose first line is a shebang are considered: this excludes
    test files and documentation that merely mention the ``# /// script``
    marker in prose or in an embedded example.
    """
    candidates = (
        *REPOSITORY_ROOT.glob("**/*.py"),
        *REPOSITORY_ROOT.glob("**/*.py.jinja"),
    )
    scripts = []
    for path in candidates:
        if ".git" in path.parts or path == pathlib.Path(__file__).resolve():
            continue
        lines = path.read_text("utf-8").splitlines()
        if lines and lines[0].startswith("#!") and PEP723_MARKER in lines[:5]:
            scripts.append(path)
    return scripts


def test_no_pep723_script_ships_the_broken_shebang() -> None:
    """No script that declares inline metadata uses the argument-eating form."""
    scripts = _scripts_with_pep723_metadata()
    assert scripts, "expected at least one PEP 723 script in the repository"

    offenders = [
        path
        for path in scripts
        if path.read_text("utf-8").splitlines()[0] == BROKEN_SHEBANG
    ]

    assert offenders == [], (
        f"scripts still use the broken shebang: {offenders}. "
        f"Use {CORRECT_SHEBANG!r} instead so uv installs declared dependencies."
    )


def test_pep723_scripts_use_the_prescribed_shebang() -> None:
    """Every PEP 723 script begins with the prescribed ``uv run --script`` form."""
    scripts = _scripts_with_pep723_metadata()

    for path in scripts:
        first_line = path.read_text("utf-8").splitlines()[0]
        assert first_line == CORRECT_SHEBANG, (
            f"{path} has shebang {first_line!r}, expected {CORRECT_SHEBANG!r}"
        )


@pytest.mark.slow
def test_prescribed_shebang_installs_declared_dependency_before_execution(
    tmp_path: pathlib.Path,
) -> None:
    """A directly invoked script can import a dependency declared via PEP 723.

    This reproduces the failure the broken shebang causes: ``uv run python``
    ignores the inline metadata block, so ``import packaging`` would raise
    ``ModuleNotFoundError`` unless the dependency happened to be preinstalled.
    ``uv run --script`` reads the block and installs ``packaging`` first.
    """
    uv_executable = shutil.which("uv")
    if uv_executable is None:
        pytest.skip("uv is unavailable to execute the PEP 723 script")

    script = tmp_path / "check_packaging_version.py"
    script.write_text(
        textwrap.dedent(
            f"""\
            {CORRECT_SHEBANG}
            # /// script
            # requires-python = ">=3.13"
            # dependencies = ["packaging"]
            # ///
            \"\"\"Print the packaging distribution's version to prove import success.\"\"\"

            import packaging

            print(packaging.__version__)
            """
        ),
        encoding="utf-8",
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)

    result = subprocess.run(  # noqa: S603 - argv is a trusted, self-authored temp script.
        [str(script)],
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )

    assert result.returncode == 0, (
        f"prescribed shebang failed to run: stdout={result.stdout!r} "
        f"stderr={result.stderr!r}"
    )
    assert result.stdout.strip(), "expected the script to print a version string"
