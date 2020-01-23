version := $(shell cat version.txt)
full_name := sverrirab/icenews

.PHONY: test lint build push

lint:
	black --check .
	flake8 icenews test

test: lint
	pytest

build:
	docker build -t icenews --build-arg VERSION=$(version) .

push:
	docker tag icenews $(full_name):$(version)
	docker tag icenews $(full_name):latest
	docker push $(full_name):$(version)
	docker push $(full_name):latest
