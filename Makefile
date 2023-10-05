SHELL := /bin/bash

.PHONY: all
all: install-dependencies

.PHONY: build
build:
	echo "# TODO(antoniae)"

.PHONY: clean
clean:
	echo "# TODO(antoniae)"

.PHONY: install-dependencies
install-dependencies:
	pip install -r requirements.txt

.PHONY: lint
lint:
	echo "# TODO(antoniae)"

.PHONY: test
test:
	mkdir -p sim
	cd sim && pytest ..