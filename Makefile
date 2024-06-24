#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
OS := $(shell $(PYTHON) -c "import sys; print('win32' if sys.platform == 'win32' else 'unix')")
PORT := 8997

ifeq ($(OS),win32)
	PYTHONPATH := $(shell $(PYTHON) -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml tests/
else
	PYTHONPATH := $(shell pwd)
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml tests/
endif

.PHONY: lock install-dev install-prod install pre-commit-install start-dev start \
        stop-prod deploy migrate download-log pre-commit-uninstall polish-codestyle \
        formatting test check-codestyle lint build-by-docker-dev build-by-docker \
        pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove \
        pytestcache-remove build-remove cleanup help

lock:
	poetry lock -n && poetry export --without-hashes > requirements.txt

install-dev:
	poetry install -n --with dev

install-prod:
	poetry install -n --with prod

install:
	@$(MAKE) install-dev

pre-commit-install:
	poetry run pre-commit install

start-dev: install-dev
ifeq ($(OS),win32)
	@if not exist "./static" poetry run python manage.py collectstatic
else
	@if [ ! -d "./static" ]; then \
		poetry run python manage.py collectstatic; \
	fi
endif
	poetry run python manage.py runserver ${PORT}

start:
	python manage.py runserver ${PORT}

stop:
	@scripts/local/stop.sh

stop-prod:
	@scripts/local/stop.sh

deploy:
	@scripts/deploy/build-docker.sh

migrate:
	poetry run python manage.py migrate
	poetry run python manage.py makemigrations

download-log:
	poetry run download-log

pre-commit-uninstall:
	poetry run pre-commit uninstall

polish-codestyle:
	poetry run ruff format --config pyproject.toml .
	poetry run ruff check --fix --config pyproject.toml .

formatting:
	@$(MAKE) polish-codestyle

test:
	$(TEST_COMMAND)

check-codestyle:
	poetry run ruff format --check --config pyproject.toml app commons wisdom_engineering services jobs
	poetry run ruff check --config pyproject.toml .

lint:
	@$(MAKE) check-codestyle

build-by-docker-dev:
	@scripts/local/build-docker.sh

build-by-docker:
	@$(MAKE) build-by-docker-dev

pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

mypycache-remove:
	find . | grep -E ".mypy_cache" | xargs rm -rf

ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

build-remove:
	rm -rf build/

cleanup:
	@$(MAKE) pycache-remove
	@$(MAKE) dsstore-remove
	@$(MAKE) mypycache-remove
	@$(MAKE) ipynbcheckpoints-remove
	@$(MAKE) pytestcache-remove
	@$(MAKE) build-remove

help:
	@echo "Available targets:"
	@echo "  lock                 - Lock the poetry dependencies and export to requirements.txt"
	@echo "  install-dev          - Install development dependencies"
	@echo "  install-prod         - Install production dependencies"
	@echo "  install              - Alias for install-dev"
	@echo "  pre-commit-install   - Install pre-commit hooks"
	@echo "  start-dev            - Start the development server"
	@echo "  start                - Alias for start-dev"
	@echo "  stop-prod            - Stop the production server"
	@echo "  deploy               - Deploy the application using Docker"
	@echo "  migrate              - Run database migrations"
	@echo "  download-log         - Download logs"
	@echo "  pre-commit-uninstall - Uninstall pre-commit hooks"
	@echo "  polish-codestyle     - Format code using ruff and check for errors"
	@echo "  formatting           - Alias for polish-codestyle"
	@echo "  test                 - Run tests"
	@echo "  check-codestyle      - Check code style with ruff"
	@echo "  lint                 - Alias for check-codestyle"
	@echo "  build-by-docker-dev  - Build the Docker container for development"
	@echo "  build-by-docker      - Alias for build-by-docker-dev"
	@echo "  cleanup              - Remove Python cache files, .DS_Store files, etc."
	@echo "  help                 - Display this help message"
