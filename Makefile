version := $(shell cat version.txt)
full_name := sverrirab/icenews

.PHONY: test lint build push

all: lint test build

lint:
	black --check .
	flake8 icenews tests

test:
	pytest

pypi:
	python setup.py bdist_wheel
	twine upload dist/icenews-$(version)-py3-none-any.whl

build:
	docker build --no-cache -t icenews --build-arg VERSION=$(version) .

push:
	docker tag icenews $(full_name):$(version)
	docker tag icenews $(full_name):latest
	docker push $(full_name):$(version)
	docker push $(full_name):latest
