
ROOT_PATH=$(shell pwd)
SETTINGS_PATH=$(ROOT_PATH)/config
PACKAGE_NAME=mockernaut
PACKAGE_PATH=$(ROOT_PATH)/$(PACKAGE_NAME)
TESTS_PATH=$(ROOT_PATH)/tests

PIP_BIN=pip
MYSQL_BIN=mysql
PEP8_BIN=pep8

TEST_RUNNER=nosetests
TEST_DATABASE_USER=root
TEST_DATABASE_NAME=$(PACKAGE_NAME)_test


all: help

help:
	@echo "help - display this help."
	@echo "init - install project requirements."
	@echo "inittest - install tests requirements."
	@echo "inittestdb - create tests database and loads schema."
	@echo "test - run tests"
	@echo "initdev - install development tools."
	@echo "runserver - run application on development server."
	@echo "clean - clean all artifacts."
	@echo "clean-build - remove build artifacts."
	@echo "clean-pyc - remove Python file artifacts."
	@echo "check - check package code style via pep8 utility."

init:
	$(PIP_BIN) install -r requirements.txt

inittest:
	$(PIP_BIN) install -r test-requirements.txt

inittestdb:
	$(MYSQL_BIN) -u$(TEST_DATABASE_USER) -e 'CREATE DATABASE IF NOT EXISTS $(TEST_DATABASE_NAME)'
	$(MYSQL_BIN) -u$(TEST_DATABASE_USER) $(TEST_DATABASE_NAME) < $(PACKAGE_NAME)/sql/schema.sql

test: inittestdb
	MOCKERNAUT_SETTINGS=$(SETTINGS_PATH)/test_config.py $(TEST_RUNNER) -v --nocapture $(TESTS_PATH)

initdev:
	$(PIP_BIN) install -r dev-requirements.txt

runserver:
	PYTHONPATH=$(PYTHONPATH):$(ROOT_PATH) \
	MOCKERNAUT_SETTINGS=${SETTINGS_PATH}/dev_config.py \
	$(ROOT_PATH)/bin/runserver.py

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
	$(PEP8_BIN) --exclude=dictconfig.py $(PACKAGE_PATH) $(TESTS_PATH)
