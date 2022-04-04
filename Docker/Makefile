PROJECT_DIR = cryptostock_api
CODE_DIR = cryptostock

all: | install-poetry export-requirements container_up

.PHONY: install-poetry
install-poetry:
	cd .. && pip install poetry

.PHONY: export-requirements
export-requirements:
	cd ../$(PROJECT_DIR) && poetry export -f requirements.txt --output requirements.txt --dev --without-hashes && mv requirements.txt $(CODE_DIR)/

.PHONY: container_up
container_up:
	docker-compose up
