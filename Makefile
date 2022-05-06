help:                             ## Display a help message detailing commands and their purpose
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

## [DEV ENV SETUP]
build:                            ## builds the container for production
	ENVIRONMENT=production docker-compose up -d --build --force-recreate --remove-orphans

build-dev:                        ## builds the container with the development flag
	ENVIRONMENT=development docker-compose up -d --build --force-recreate --remove-orphans

## [UTILS]
requirements-build:               ## run pip compile and add requirements from the *.in files
	pip-compile -o requirements.txt requirements.in && pip-compile -o requirements-dev.txt requirements-dev.in

requirements-update:              ## run pip compile and rebuild the requirements files
	pip-compile -r -U -o requirements.txt requirements.in && pip-compile -r -U -o requirements-dev.txt requirements-dev.in && chmod a+r requirements.txt && chmod a+r requirements-dev.txt

## [CODE CHECKING]
format:                           ## format the code
	black --line-length=120 --target-version=py310 ./app

format-check:                     ## check the code is formatted
	black --line-length=120 --target-version=py310 --check --diff ./app
