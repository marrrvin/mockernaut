
ROOT_PATH=$(shell pwd)

SETTINGS_PATH=$(ROOT_PATH)/config
PACKAGE_NAME=mockernaut
PACKAGE_PATH=$(ROOT_PATH)/$(PACKAGE_NAME)
TESTS_PATH=$(ROOT_PATH)/tests
BIN_PATH=$(ROOT_PATH)/bin
TEST_DATABASE_NAME=mockernaut_test


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
	pip install -r requirements.txt --use-mirrors

inittest:
	pip install -r test-requirements.txt --use-mirrors

inittestdb:
	mysql -uroot -e 'CREATE DATABASE IF NOT EXISTS $(TEST_DATABASE_NAME)'
	mysql -uroot $(TEST_DATABASE_NAME) < $(PACKAGE_NAME)/sql/schema.sql

test: inittest inittestdb
	MOCKERNAUT_SETTINGS=$(SETTINGS_PATH)/test_config.py nosetests -v $(TESTS_PATH)

initdev:
	pip install -r dev-requirements.txt --use-mirrors

runserver:
	PYTHONPATH=$(PYTHONPATH):$(ROOT_PATH) MOCKERNAUT_SETTINGS=${SETTINGS_PATH}/dev_config.py $(BIN_PATH)/runserver.py

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
	pep8 --exclude=dictconfig.py $(PACKAGE_PATH) $(TESTS_PATH)
