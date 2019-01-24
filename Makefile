VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate

PWD = $(shell pwd)

$(VENV):
	virtualenv .venv
	$(VENV_ACTIVATE); pip install tox
	$(VENV_ACTIVATE); pip install -e .

.PHONY: test
test: clean $(VENV)
	cd $(PWD)/tests/test-two-envs && tox
	cd $(PWD)/tests/test-env-inheritance && tox

clean:
	rm -rf $(VENV)
	find tests -name .tox -type d -exec rm -r "{}" +
