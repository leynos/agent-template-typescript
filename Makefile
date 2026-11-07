.PHONY: check-fmt fmt lint typecheck spelling test help

MDLINT ?= $(shell command -v markdownlint-cli2 2>/dev/null || printf '%s' "$$HOME/.bun/bin/markdownlint-cli2")
# `make fmt` and `make check-fmt` call mdtablefix directly. `--git` selects the
# Markdown files Git tracks and `--include-untracked` adds the untracked files
# Git does not ignore, so a new document is formatted before it is staged.
# Both modes need mdtablefix 0.6.0 or later; CI pins the version at the
# install-mdtablefix step.
MDTABLEFIX ?= mdtablefix
MDTABLEFIX_SELECT = --git --include-untracked
MDTABLEFIX_RULES = --wrap --renumber --breaks --ellipsis --fences

# Check Markdown formatting without making changes; the template root has no
# source files of its own.
check-fmt:
	$(MDTABLEFIX) --check $(MDTABLEFIX_SELECT) $(MDTABLEFIX_RULES)

fmt: ## Format Markdown sources
	$(MDTABLEFIX) --in-place $(MDTABLEFIX_SELECT) $(MDTABLEFIX_RULES)
	$(MDLINT) --fix "**/*.md"

# Run linter
# The repository's Python is the typos roll-out helpers (also copied under
# template/scripts) and the tests. Interrogate scans each target recursively,
# subject to its default exclusions.
INTERROGATE_VERSION ?= 1.7.0
INTERROGATE_TARGETS ?= scripts template tests
# Level 2 prints a MISSED row per undocumented definition, which the
# `interrogate` recipe below looks for: the rounded percentage alone can pass a
# lone gap.
INTERROGATE_FLAGS ?= -vv --fail-under 100
INTERROGATE ?= uv tool run --python 3.13 --from 'interrogate==$(INTERROGATE_VERSION)' interrogate

# Interrogate rounds its percentage to one decimal, so `--fail-under 100` alone
# can pass a lone gap in a large repository. This recipe also fails when `grep`
# finds a MISSED row in the report on standard output, which `-vv` or higher
# prints for each undocumented definition.
.PHONY: interrogate
interrogate: ## Enforce complete Python docstring coverage
	@report="$$($(INTERROGATE) $(INTERROGATE_FLAGS) $(INTERROGATE_TARGETS))"; \
	  status=$$?; \
	  printf '%s\n' "$$report"; \
	  test "$$status" -eq 0 || exit "$$status"; \
	  if printf '%s\n' "$$report" | grep -q '| *MISSED *|'; then \
	    printf '%s\n' 'interrogate: undocumented definitions remain; see the MISSED rows above' >&2; \
	    exit 1; \
	  fi

lint:
	$(MAKE) --no-print-directory interrogate
	@echo "No source files to lint in template root"

# Run type checker
typecheck:
	@echo "No source files to typecheck in template root"

test: ## Run template tests
	uvx --with pytest-copier --with hypothesis pytest tests/

TYPOS_VERSION ?= 1.48.0
TYPOS := uv tool run typos@$(TYPOS_VERSION)

spelling: ## Enforce en-GB-oxendict spelling in parent and template prose
	uv run scripts/generate_typos_config.py
	find . -type f \( -name '*.md' -o -name '*.md.jinja' \) -not -path './.git/*' -print0 | \
		xargs -0 $(TYPOS) --config typos.toml --force-exclude

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS=":.*?## "; printf "Available targets:\n"} {printf "  %-15s %s\n", $$1, $$2}'
