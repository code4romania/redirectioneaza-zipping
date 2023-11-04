help:                             ## Display a help message detailing commands and their purpose
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

## [Managing the project]
### Stopping the containers
stop-prod:                        ## stops the containers for production
	docker-compose -f docker-compose.prod.yml down

stop-dev:                         ## stops the containers for dev
	docker-compose down

stop: stop-dev                    ## stops the containers for dev


# Building and running the containers
run-prod:                         ## builds the container for production
	docker-compose -f docker-compose.prod.yml up --build --force-recreate --remove-orphans

rund-prod:                         ## builds the container for production in detached mode
	docker-compose -f docker-compose.prod.yml up -d --build --force-recreate --remove-orphans

run-dev:                          ## builds and runs the container for dev
	docker-compose up --build --force-recreate --remove-orphans

rund-dev:                          ## builds and runs the container for dev in detached mode
	docker-compose up -d --build --force-recreate --remove-orphans

run: run-dev                       ## builds and runs the container for dev
rund: rund-dev                     ## builds and runs the container for dev in detached mode

## [UTILS]
requirements-build:               ## run pip compile and add requirements from the *.in files
	pip-compile -o requirements.txt requirements.in && pip-compile -o requirements-dev.txt requirements-dev.in

requirements-update:              ## run pip compile and rebuild the requirements files
	pip-compile -r -U -o requirements.txt requirements.in && pip-compile -r -U -o requirements-dev.txt requirements-dev.in && chmod a+r requirements.txt && chmod a+r requirements-dev.txt

## [CODE CHECKING]
format:                           ## format the code
	black --line-length=120 --target-version=py311 ./app

format-check:                     ## check the code is formatted
	black --line-length=120 --target-version=py311 --check --diff ./app

