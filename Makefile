VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate

PWD = $(shell pwd)

TOX = tox

$(VENV):
	virtualenv .venv
	$(VENV_ACTIVATE); pip install tox
	$(VENV_ACTIVATE); pip install -e .

lint: $(VENV)
	tox -e flake8

.PHONY: test
test: clean $(VENV) lint
	cd $(PWD)/tests/test-two-envs && $(TOX)
	cd $(PWD)/tests/test-env-inheritance && $(TOX)
	cd $(PWD)/tests/test-environment-variable && ./run-tox.sh $(TOX)

clean:
	rm -rf $(VENV)
	find tests -name .tox -type d -exec rm -r "{}" +
