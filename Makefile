.PHONY: test
test:
	@ coverage run --source='.' `which pytest`
	@ coverage html -d coverage_report
	@ coverage xml -o coverage.xml
	@ coverage report
	@echo "Running mypy checks..."
	@ mypy src/versup --ignore-missing-imports --check-untyped-defs
	@echo "Running ruff checks"
	@ ruff check src 
	@echo "Running Black"
	@ black --check src