VENV = .venv
VENV_ACTIVATE = . $(VENV)/bin/activate

$(VENV):
	virtualenv .venv
	$(VENV_ACTIVATE); pip install tox
	$(VENV_ACTIVATE); pip install -e .

.PHONY: test
test: clean $(VENV)
	cd tests && tox

clean:
	rm -rf $(VENV)
	rm -rf tests/.tox
