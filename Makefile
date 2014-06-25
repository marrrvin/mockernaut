
PYTHONPATH=${PYTHONPATH}:$(shell pwd)/
MOCKERNAUT_SETTINGS_PATH=$(shell pwd)/config/


help:
	@echo "init - install project requirements."
	@echo "test - run tests"
	@echo "runserver - run application on development server."
	@echo "clean - clean all artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"

init:
	pip install -r requirements.txt --use-mirrors

test:
	MOCKERNAUT_SETTINGS=${MOCKERNAUT_SETTINGS_PATH}/test_config.py python -m unittest discover -v tests

runserver:
	MOCKERNAUT_SETTINGS=${MOCKERNAUT_SETTINGS_PATH}/develop_config.py bin/runserver.py

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
