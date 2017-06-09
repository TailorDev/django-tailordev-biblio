default: help

VENV_NAME = venv
VENV_PATH = $(shell pwd)/$(VENV_NAME)
PIP       = $(VIRTUAL_ENV) $(VENV_PATH)/bin/pip
PYTHON    = $(VIRTUAL_ENV) $(VENV_PATH)/bin/python
PYTEST    = $(VIRTUAL_ENV) $(VENV_PATH)/bin/py.test
MANAGE    = $(DATABASE_URL) $(PYTHON) sandbox/manage.py

VIRTUAL_ENV  = VIRTUAL_ENV="$(VENV_PATH)"
DATABASE_URL = DATABASE_URL="sqlite:///$(shell pwd)/sandbox/db.sqlite3"
TESTS_DATABASE_URL = DATABASE_URL="sqlite:///:memory:"

venv:  ## create the python virtual env
	@python3 -m venv $(VENV_NAME)

bootstrap: venv  ## bootstrap the application
	@$(PIP) install -r requirements/dev.txt
	@$(PYTHON) setup.py develop
	@$(MANAGE) migrate
.PHONY: bootstrap

dev: venv  ## start the development server
	@$(MANAGE) runserver
.PHONY: dev

migrate: venv  ## perform database migrations
	@$(MANAGE) migrate
.PHONY: migrate

test: venv  ## run the test suite
	@$(TESTS_DATABASE_URL) $(PYTEST)
.PHONY: test

help:
	@echo "// Django TailorDev Biblio"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
