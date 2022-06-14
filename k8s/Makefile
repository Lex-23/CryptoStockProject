PROJECT_DIR = cryptostock_api
BE_CODE_DIR = cryptostock
NOTIFICATION_SERVICES_DIR = cryptostock_notification_services
UI_APP_PATH = ui/cryptostock_app/

STAGE = dev
BE_BUILD_TAG = 1.0.0
NOTIFICATION_BOTS_IMAGE_TAG = 1.0.0
UI_BUILD_TAG = 1.0.0

DB_MANIFEST = postgres
BE_MANIFEST = be_django
REDIS_MANIFEST = redis
CELERY_MANIFEST = celery
TG_BOT_MANIFEST = tg_bot
VK_BOT_MANIFEST = vk_bot
UI_MANIFEST = fe_react

export DNS=cryptostock.market.sample
export BE_IMAGE_NAME="be-${STAGE}:${BE_BUILD_TAG}"
export NOTIFICATION_BOTS_IMAGE_NAME="notification_bots-${STAGE}:${NOTIFICATION_BOTS_IMAGE_TAG}"
export NODE_IP=192.168.49.2
export APP_PORT=8543
export UI_IMAGE_NAME="ui-${STAGE}:${UI_BUILD_TAG}"
export REACT_APP_BASE_URL="http://${DNS}/api/"

all: | start-minikube export-requirements-app be-build apply-namespace \
	   apply-configmap apply-db-manifest apply-be-manifest apply-redis-manifest \
	   apply-celery-manifest export-requirements-notification-services \
	   notification-services-build apply-tg-bot-manifest apply-vk-bot-manifest \
	   create-ui-builder build-ui apply-ui-manifest apply-ingress-manifest


.PHONY: start-minikube
# create local cluster and use minikube docker daemon instead host docker daemon
start-minikube:
	minikube start && eval $$(minikube docker-env)

.PHONY: export-requirements-app
export-requirements-app:
	cd ../$(PROJECT_DIR) && \
	poetry export -f requirements.txt --output requirements.txt --dev --without-hashes && \
	mv requirements.txt $(BE_CODE_DIR)/

.PHONY: be-build
be-build:
	cd ../$(PROJECT_DIR)/$(BE_CODE_DIR) && \
	docker build -t $(BE_IMAGE_NAME) .

.PHONY: apply-namespace
apply-namespace:
	kubectl apply -f "${STAGE}-namespace.yaml"

.PHONY: apply-configmap
apply-configmap:
	envsubst < "${STAGE}-configmap.yaml" | kubectl apply -f -

.PHONY: apply-db-manifest
apply-db-manifest:
	kubectl apply -f $(DB_MANIFEST)

.PHONY: apply-be-manifest
apply-be-manifest:
	kubectl apply -f $(BE_MANIFEST)/ && \
	envsubst < $(BE_MANIFEST)/deployment.yaml | kubectl apply -f -

.PHONY: apply-redis-manifest
apply-redis-manifest:
	kubectl apply -f $(REDIS_MANIFEST)

.PHONY: apply-celery-manifest
apply-celery-manifest:
	kubectl apply -f $(CELERY_MANIFEST)/ && \
	envsubst < $(CELERY_MANIFEST)/beat-deployment.yaml | kubectl apply -f - && \
	envsubst < $(CELERY_MANIFEST)/flower-deployment.yaml | kubectl apply -f - && \
	envsubst < $(CELERY_MANIFEST)/worker-deployment.yaml | kubectl apply -f -

.PHONY: export-requirements-notification-services
export-requirements-notification-services:
	cd ../$(NOTIFICATION_SERVICES_DIR) && \
	poetry export -f requirements.txt --output requirements.txt --dev --without-hashes

.PHONY: notification-services-build
notification-services-build:
	cd ../$(NOTIFICATION_SERVICES_DIR) && \
	docker build -t $(NOTIFICATION_BOTS_IMAGE_NAME) .

.PHONY: apply-tg-bot-manifest
apply-tg-bot-manifest:
	envsubst < $(TG_BOT_MANIFEST)/deployment.yaml | kubectl apply -f -

.PHONY: apply-vk-bot-manifest
apply-vk-bot-manifest:
	envsubst < $(VK_BOT_MANIFEST)/deployment.yaml | kubectl apply -f -

.PHONY: create-ui-builder
create-ui-builder:
	cd ../$(UI_APP_PATH) && docker build -t fe-build:latest --build-arg REACT_APP_BASE_URL .

.PHONY: build-ui
build-ui:
	cd fe_react/ && docker build -t $(UI_IMAGE_NAME) .

.PHONY: apply-ui-manifest
apply-ui-manifest:
	kubectl apply -f $(UI_MANIFEST)/ && \
	envsubst < $(UI_MANIFEST)/deployment.yaml | kubectl apply -f -

.PHONY: apply-ingress-manifest
apply-ingress-manifest:
	kubectl apply -f "${STAGE}-ingress.yaml"
