SHELL := /bin/sh

PROJECT := config
PROJECT_DIR := $(abspath $(shell pwd))

pre_commit_all:
	pre-commit install
	pre-commit run --all-files

test:
	coverage erase
	coverage run manage.py test
	coverage combine
	coverage report
	coverage erase

deploy_production:
	./manage.py test
	echo "Add deployment code here... ;)"
