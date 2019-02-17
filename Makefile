.PHONY: lint test clean clean-dist bump release

VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate
BUMPTYPE = patch

PWD = $(shell pwd)

TOX = tox

$(VENV):
	virtualenv $(VENV)
	$(VENV_ACTIVATE); pip install tox bumpversion twine 'readme_renderer[md]'
	$(VENV_ACTIVATE); pip install -e .

lint: $(VENV)
	$(VENV_ACTIVATE); tox -e flake8

test: clean-tests $(VENV) lint
	$(VENV_ACTIVATE); cd $(PWD)/tests/test-two-envs && $(TOX)
	$(VENV_ACTIVATE); cd $(PWD)/tests/test-env-inheritance && $(TOX)
	$(VENV_ACTIVATE); cd $(PWD)/tests/test-environment-variable && ./run-tox.sh $(TOX)

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

clean-tests:
	find tests -name .tox -type d -exec rm -r "{}" +

clean: clean-dist clean-tests
	rm -rf $(VENV)


