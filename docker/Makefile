PROJECT_DIR = cryptostock_api
BE_CODE_DIR = cryptostock
BE_BUILD_DIR = ../cryptostock_api/cryptostock/
NOTIFICATION_SERVICES_DIR = cryptostock_notification_services
BE_BUILD_IMAGE_NAME = be_build:latest
ENV_FILE = docker.dev.env

all: | install-poetry export-requirements-app be-build export-requirements_notification_services containers-up


.PHONY: install-poetry
install-poetry:
	cd .. && pip install poetry

.PHONY: export-requirements-app
export-requirements-app:
	cd ../$(PROJECT_DIR) && \
		poetry export -f requirements.txt --output requirements.txt --dev --without-hashes && \
		mv requirements.txt $(BE_CODE_DIR)/

.PHONY: be-build
be-build:
	cp $(ENV_FILE) $(BE_BUILD_DIR) && \
	docker build $(BE_BUILD_DIR) -t $(BE_BUILD_IMAGE_NAME)


.PHONY: export-requirements_notification_services
export-requirements_notification_services:
	cd ../$(NOTIFICATION_SERVICES_DIR) && \
		poetry export -f requirements.txt --output requirements.txt --dev --without-hashes

.PHONY: containers-up
containers-up:
	docker-compose up
