.PHONY: check-fmt lint typecheck test test-all fmt

# Check formatting without making changes
check-fmt:
	@echo "No source files to check in template root"

# Run linter
lint:
	@echo "No source files to lint in template root"

# Run type checker
typecheck:
	@echo "No source files to typecheck in template root"

# Run tests
test:
	@echo "No tests in template root - generate a project to test"

# Run all checks
test-all: check-fmt lint typecheck test
