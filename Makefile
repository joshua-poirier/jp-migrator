.PHONY: init
init:
	pip install pipenv
	pipenv install --dev

.PHONY: lint
lint:
	python -m flake8 .

.PHONY: check_format
check_format: lint
	python -m black . --check

.PHONY: format
format: lint
	python -m isort .
	python -m black .

.PHONY: test
test: lint format
	pipenv run pytest tests

.PHONY: coverage
coverage:
	pipenv run pytest --cov=src tests
