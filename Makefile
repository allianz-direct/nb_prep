install:
	pip install .
	pip install -r dev_requirements.txt

test:
	pytest

ci: install test