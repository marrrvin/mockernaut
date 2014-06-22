
init:
	pip install -r requirements.txt --use-mirrors

test:
	PYTHONPATH=${PYTHONPATH}:$(shell pwd)/ MOCKERNAUT_SETTINGS=$(shell pwd)/config/test_config.py python -m unittest discover -v tests

runserver:
	PYTHONPATH=${PYTHONPATH}:$(shell pwd)/ MOCKERNAUT_SETTINGS=$(shell pwd)/config/develop_config.py bin/runserver.py
