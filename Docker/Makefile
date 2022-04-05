PROJECT_DIR = cryptostock_api
CODE_DIR = cryptostock

all: | install-poetry export-requirements containers-up

.PHONY: install-poetry
install-poetry:
	cd .. && pip install poetry

.PHONY: export-requirements
export-requirements:
	cd ../$(PROJECT_DIR) && \
		poetry export -f requirements.txt --output requirements.txt --dev --without-hashes && \
		mv requirements.txt $(CODE_DIR)/

.PHONY: containers-up
containers-up:
	docker-compose up
