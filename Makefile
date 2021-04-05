.PHONY: test
test:
	@ coverage run --source='.' `which pytest`
	@ coverage html -d coverage_report
	@ coverage xml -o coverage.xml
	@ coverage report
	@ flake8 versup
	@ mypy versup --ignore-missing-imports