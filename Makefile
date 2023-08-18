up:
	@poetry update

deps:
	@poetry install --no-root

test: deps
	pytest

exp: up
	@poetry export --output config/requirements.txt
	@poetry export -f requirements.txt --output config/requirements-prod.txt --without-hashes

build: deps
	@poetry build

run: deps
	poetry run start
