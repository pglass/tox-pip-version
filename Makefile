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

test: clean-tests $(VENV) lint test-tox-3.7 test-tox-3.8

# TODO: Need to refactor to test more pip versions
test-tox-3.8: clean-tests
	$(VENV_ACTIVATE); pip install 'tox>=3.8,<3.9'
	$(VENV_ACTIVATE); cd $(PWD)/tests/test-two-envs && $(TOX)
	$(VENV_ACTIVATE); cd $(PWD)/tests/test-env-inheritance && $(TOX)
	$(VENV_ACTIVATE); cd $(PWD)/tests/test-environment-variable && ./run-tox.sh $(TOX)

test-tox-3.7: clean-tests
	$(VENV_ACTIVATE); pip install 'tox>=3.7,<3.8'
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


