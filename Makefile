
PYTHONPATH=${PYTHONPATH}:$(shell pwd)/
MOCKERNAUT_SETTINGS_PATH=$(shell pwd)/config/


help:
	@echo "init - install project requirements."
	@echo "test - run tests"
	@echo "runserver - run application on development server."

init:
	pip install -r requirements.txt --use-mirrors

test:
	MOCKERNAUT_SETTINGS=${MOCKERNAUT_SETTINGS_PATH}/test_config.py python -m unittest discover -v tests

runserver:
	MOCKERNAUT_SETTINGS=${MOCKERNAUT_SETTINGS_PATH}/develop_config.py bin/runserver.py
