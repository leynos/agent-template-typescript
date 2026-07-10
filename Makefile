.PHONY: check-fmt lint typecheck spelling test help

# Check formatting without making changes
check-fmt:
	@echo "No source files to check in template root"

# Run linter
lint:
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
