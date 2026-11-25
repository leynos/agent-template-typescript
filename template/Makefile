.PHONY: help all clean build lint fmt check-fmt typecheck test markdownlint spelling

.DEFAULT_GOAL := all

all: build check-fmt lint typecheck test
	+$(MAKE) spelling

node_modules: package.json
	bun install
	@touch node_modules

build: node_modules ## Install dependencies

clean: ## Remove build artifacts
	rm -rf dist node_modules .bun
	rm -f .typos-oxendict-base.json .typos-oxendict-base.toml

fmt: build ## Format sources
	bun run fmt
	mdformat-all

check-fmt: build ## Verify formatting
	bunx biome check --formatter-enabled=true --linter-enabled=false src tests

lint: build ## Run linters
	bun run lint

typecheck: build ## Run type checking
	bun run check:types

test: build ## Run tests
	bun test

markdownlint: ## Lint Markdown files
	bunx markdownlint-cli2 '**/*.md'
	+$(MAKE) spelling

TYPOS_CONFIG_BUILDER_VERSION ?= v0.1.4
TYPOS_CONFIG_BUILDER = uv tool run --python 3.14 --from \
	"git+https://github.com/leynos/typos-config-builder.git@$(TYPOS_CONFIG_BUILDER_VERSION)" \
	typos-config-builder

# The gate reads tracked files only; stage new Markdown before expecting it checked.
spelling: ## Enforce en-GB-oxendict spelling in prose
	$(TYPOS_CONFIG_BUILDER) gate --repository .

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
	sed 's/:.*##/##/' | \
	awk 'BEGIN {FS="##"; printf "Available targets:\n"} {gsub(/^[ \t]+/, "", $$2); printf "  %-20s %s\n", $$1, $$2}'
