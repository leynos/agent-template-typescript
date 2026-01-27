.PHONY: check-fmt lint typecheck test help

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
	uvx --with pytest-copier pytest tests/

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS=":.*?## "; printf "Available targets:\n"} {printf "  %-15s %s\n", $$1, $$2}'
