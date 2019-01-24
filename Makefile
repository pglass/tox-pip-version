.PHONY: lint test clean clean-dist bump release

VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate
BUMPTYPE = patch

PWD = $(shell pwd)

TOX = tox

$(VENV):
	virtualenv .venv
	$(VENV_ACTIVATE); pip install tox bumpversion twine
	$(VENV_ACTIVATE); pip install -e .

lint: $(VENV)
	tox -e flake8

test: clean $(VENV) lint
	cd $(PWD)/tests/test-two-envs && $(TOX)
	cd $(PWD)/tests/test-env-inheritance && $(TOX)
	cd $(PWD)/tests/test-environment-variable && ./run-tox.sh $(TOX)

dist: clean-dist
	python setup.py sdist
	ls -ls dist
	tar tzf dist/*

bump: $(VENV)
	$(VENV_ACTIVATE); bumpversion $(BUMPTYPE)
	git show -q
	@echo
	@echo "SUCCESS: Version was bumped and committed. Now push the commit."
	@echo
	@echo "    git push origin master && git push --tags"

release: test dist
	$(VENV_ACTIVATE); twine upload dist/*

clean-dist:
	rm -rf dist

clean: clean-dist
	rm -rf $(VENV)
	find tests -name .tox -type d -exec rm -r "{}" +
