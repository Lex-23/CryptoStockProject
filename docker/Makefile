PROJECT_DIR = cryptostock_api
CODE_DIR = cryptostock
BE_BUILD_DIR = ../cryptostock_api/cryptostock/
BE_BUILD_IMAGE_NAME = be_build:latest
ENV_FILE = docker.dev.env

all: | install-poetry export-requirements be-build containers-up


.PHONY: install-poetry
install-poetry:
	cd .. && pip install poetry

.PHONY: export-requirements
export-requirements:
	cd ../$(PROJECT_DIR) && \
		poetry export -f requirements.txt --output requirements.txt --dev --without-hashes && \
		mv requirements.txt $(CODE_DIR)/

.PHONY: be-build
be-build:
	cp $(ENV_FILE) $(BE_BUILD_DIR) && \
	docker build $(BE_BUILD_DIR) -t $(BE_BUILD_IMAGE_NAME)

.PHONY: containers-up
containers-up:
	docker-compose up
