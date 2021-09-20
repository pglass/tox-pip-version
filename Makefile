.PHONY: lint test clean clean-dist bump release

VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate
BUMPTYPE = patch

PWD = $(shell pwd)

TOX = tox

$(VENV):
	virtualenv $(VENV)
	$(VENV_ACTIVATE); pip install -r dev-requirements.txt
	$(VENV_ACTIVATE); pip install -e .

lint: $(VENV)
	$(VENV_ACTIVATE); tox -e black,flake8

test: $(VENV) lint
	$(VENV_ACTIVATE); pytest -v -n auto tests/test.py

dist: clean-dist $(VENV)
	python setup.py sdist
	ls -ls dist
	tar tzf dist/*
	$(VENV_ACTIVATE); twine check dist/*

bump: $(VENV)
	$(VENV_ACTIVATE); bumpversion $(BUMPTYPE)
	git show -q
	@echo
	@echo "SUCCESS: Version was bumped and committed. Now push the commit."
	@echo
	@echo "    git push origin master && git push --tags"

test-release: clean test dist
	$(VENV_ACTIVATE); twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: clean test dist
	$(VENV_ACTIVATE); twine upload dist/*

clean-dist:
	rm -rf dist
	rm -rf tox_setuptools_version.egg-info

clean: clean-dist
	rm -rf $(VENV)
