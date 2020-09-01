.PHONY: test
test:
	@ black --check versup
	@ coverage run --source='.' `which pytest`
	@ coverage html -d coverage_report
	@ coverage xml -o coverage.xml
	@ coverage report