.DEFAULT: help
help:
	@echo "make test"
	@echo "       run tests"
	@echo "make setup"
	@echo "       install package"

test:
	python -m pytest

setup:
	cd problem3
	pip install .
