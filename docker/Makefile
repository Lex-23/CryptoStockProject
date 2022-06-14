PROJECT_DIR = cryptostock_api
BE_CODE_DIR = cryptostock
BE_BUILD_DIR = ../cryptostock_api/cryptostock/
FE_BUILD_DIR = ../ui/cryptostock_app/
NOTIFICATION_SERVICES_DIR = cryptostock_notification_services
BE_DOCKERFILE_NAME = Dockerfile-dev
BE_BUILD_IMAGE_NAME = be_build:latest
FE_BUILD_IMAGE_NAME = fe_build:latest
ENV_FILE = docker.dev.env

all: | install-poetry export-requirements-app be-build fe-build \
 	   export-requirements_notification_services containers-up


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
	docker build $(BE_BUILD_DIR) -f $(BE_DOCKERFILE_NAME) -t $(BE_BUILD_IMAGE_NAME)

.PHONY: fe-build
fe-build:
	docker build $(FE_BUILD_DIR) -t $(FE_BUILD_IMAGE_NAME)

.PHONY: export-requirements_notification_services
export-requirements_notification_services:
	cd ../$(NOTIFICATION_SERVICES_DIR) && \
		poetry export -f requirements.txt --output requirements.txt --dev --without-hashes

.PHONY: containers-up
containers-up:
	docker-compose up
