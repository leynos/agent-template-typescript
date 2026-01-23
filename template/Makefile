.PHONY: help all clean build lint fmt check-fmt typecheck test markdownlint

.DEFAULT_GOAL := all

all: build check-fmt lint typecheck test

node_modules: package.json
	pnpm install
	@touch node_modules

build: node_modules ## Install dependencies

clean: ## Remove build artifacts
	rm -rf dist node_modules .bun

fmt: build ## Format sources
	bun fmt

check-fmt: build ## Verify formatting
	bunx biome format --write=false src tests

lint: build ## Run linters
	bun lint

typecheck: build ## Run type checking
	bun check:types

test: build ## Run tests
	bun test

markdownlint: ## Lint Markdown files
	bunx markdownlint-cli2 '**/*.md'

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS=":"; printf "Available targets:\n"} {printf "  %-20s %s\n", $$1, $$2}'
