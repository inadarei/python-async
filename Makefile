.PHONY: default
default: install run

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run
run:
	python async_with_summary.py