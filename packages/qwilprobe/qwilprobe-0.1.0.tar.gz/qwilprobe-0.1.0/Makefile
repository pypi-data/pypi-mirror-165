.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-][a-zA-Z0-9_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

.PHONY: help
help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean
clean: ## Remove all Python artifacts
	-rm -rf dist/
	-rm -rf build/
	-find src/qwilprobe/generated ! -name '__init__.py' -delete
	-find . -name '*.egg-info' ! -path './*v*env/*' -exec rm -rf {} +
	-find . -name '*.egg' ! -path './*v*env/*' -exec rm -rf {} +
	-find . -name '*.pyc' ! -path './*v*env/*' -exec rm -rf {} +
	-find . -name '*.pyo' ! -path './*v*env/*' -exec rm -rf {} +
	-find . -name '__pycache__' ! -path './*v*env/*' -exec rm -rf {} +
	-find . -name '*~' ! -path './*v*env/*' -exec rm -rf {} +
	-rm -rf .tox/
	-rm -rf .pytest_cache/
	-rm -rf docs/qwilprobe.*.rst

.PHONY: install-dev
install-dev: ## Editable pip install of package with development dependencies
	pip install -U pip
	pip install -e .[dev]

.PHONY: bump-major
bump-major: ## Bump the major version of the package
	tox -e bump2version -- major

.PHONY: bump-minor
bump-minor: ## Bump the minor version of the package
	tox -e bump2version -- minor

.PHONY: bump-patch
bump-patch: ## Bump the patch version of the package
	tox -e bump2version -- patch

.PHONY: tests
tests: ## Run tests for the default tox environments
	tox

.PHONY: dist
dist: clean ## Build a new source and wheel distribution with tox
	@if [ -z "$$(git status --porcelain)" ]; then\
		tox -e dist;\
	else\
		echo "Dirty repo, will not build a dist!";\
		exit 1;\
	fi

.PHONY: isort
isort: ## Sort import statements in python source code
	@if [ -z "$$(git status --porcelain)" ]; then\
		tox -e isort;\
        git add .;\
        git commit -m "make isort";\
	else\
		echo "Dirty repo, will not run isort!";\
		exit 1;\
	fi

.PHONY: check-dist
check-dist: ## Check that built distributions are ok
	tox -e twine-check

.PHONY: testpypi-upload
testpypi-upload: check-dist ## Upload built distributions to TestPyPI
	tox -e pypi-upload -- --repository-url https://test.pypi.org/legacy/

.PHONY: pypi-upload
pypi-upload: check-dist ## Upload built distributions to PyPI
	tox -e pypi-upload

.PHONY: docs
docs: ## Generate documentation with Sphinx
	tox -e docs

.PHONY: flake8
flake8: ## Lint source code and test code using flake8
	tox -e flake8
