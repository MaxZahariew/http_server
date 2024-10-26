PYTHON_VERSION=3.11
VENV=.env

.PHONY: init
init:
		python$(PYTHON_VERSION) -m venv $(VENV)
		echo --- EXECUTE THE NEXT LINE ---
		echo source $(VENV)/bin/activate


.PHONY: install
install:
		poetry install


.PHONY: run
run:
		python -m uvicourn api.main:app


.PHONY: swagger
swagger:
		open -a firefox http://localhost:8000/docs


.PHONY: format
format:
		python -m black


.PHONY: test
test:
		python -m pytest