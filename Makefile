.PHONY: test
test:
	@ coverage run --source='.' `which pytest`
	@ coverage html -d coverage_report
	@ coverage xml -o coverage.xml
	@ coverage report
	@ flake8 src/versup
	@ mypy src/versup --ignore-missing-imports