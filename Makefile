
ROOT_PATH=$(shell pwd)

SETTINGS_PATH=$(ROOT_PATH)/config
PACKAGE_PATH=$(ROOT_PATH)/mockernaut
TESTS_PATH=$(ROOT_PATH)/tests
BIN_PATH=$(ROOT_PATH)/bin


all: help

help:
	@echo "help - display this help."
	@echo "init - install project requirements."
	@echo "test - run tests"
	@echo "runserver - run application on development server."
	@echo "clean - clean all artifacts."
	@echo "clean-build - remove build artifacts."
	@echo "clean-pyc - remove Python file artifacts."
	@echo "check - check package code style via pep8 utility."

init:
	pip install -r requirements.txt --use-mirrors

test:
	MOCKERNAUT_SETTINGS=$(SETTINGS_PATH)/test_config.py python -m unittest discover -v $(TESTS_PATH)

runserver:
	PYTHONPATH=$(PYTHONPATH):$(ROOT_PATH) MOCKERNAUT_SETTINGS=${SETTINGS_PATH}/develop_config.py $(BIN_PATH)/runserver.py

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

check:
	pep8 $(PACKAGE_PATH) $(TESTS_PATH)
