PROJECT_DIR = cryptostock_api
BE_CODE_DIR = cryptostock
BE_DOCKERFILE_NAME = Dockerfile-k8s
NOTIFICATION_SERVICES_DIR = cryptostock_notification_services

STAGE = dev
BE_BUILD_TAG = gamma
BE_IMAGE_NAME = be-${STAGE}:${BE_BUILD_TAG}
NOTIFICATION_BOTS_IMAGE_TAG = alfa
NOTIFICATION_BOTS_IMAGE_NAME = notification_bots-${STAGE}:${NOTIFICATION_BOTS_IMAGE_TAG}

NAMESPACE_FILE_NAME = ${STAGE}-namespace.yaml
CONFIGMAP_FILE_NAME = ${STAGE}-configmap.yaml
DB_MANIFEST = postgres/
BE_MANIFEST = be_django/
REDIS_MANIFEST = redis/
CELERY_MANIFEST = celery/
TG_BOT_MANIFEST = notification_services/tg_bot/
VK_BOT_MANIFEST = notification_services/vk_bot/

export BE_IMAGE_NAME
export NOTIFICATION_BOTS_IMAGE_NAME

all: | start-minikube export-requirements-app be-build apply-namespace \
	   apply-configmap apply-db-manifest apply-be-manifest apply-redis-manifest \
	   apply-celery-manifest export-requirements-notification-services \
	   notification-services-build apply-tg-bot-manifest apply-vk-bot-manifest

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
		docker build -f $(BE_DOCKERFILE_NAME) -t $(BE_IMAGE_NAME) .

.PHONY: apply-namespace
apply-namespace:
	kubectl apply -f $(NAMESPACE_FILE_NAME)

.PHONY: apply-configmap
apply-configmap:
	kubectl apply -f $(CONFIGMAP_FILE_NAME)

.PHONY: apply-db-manifest
apply-db-manifest:
	kubectl apply -f $(DB_MANIFEST)

.PHONY: apply-be-manifest
apply-be-manifest:
	envsubst < $(BE_MANIFEST)/deployment.yaml && \
		kubectl apply -f $(BE_MANIFEST)

.PHONY: apply-redis-manifest
apply-redis-manifest:
	kubectl apply -f $(REDIS_MANIFEST)

.PHONY: apply-celery-manifest
apply-celery-manifest:
	envsubst < $(CELERY_MANIFEST)/beat-deployment.yaml && \
	envsubst < $(CELERY_MANIFEST)/flower-deployment.yaml && \
	envsubst < $(CELERY_MANIFEST)/worker-deployment.yaml && \
		kubectl apply -f $(CELERY_MANIFEST)

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
	envsubst < $(TG_BOT_MANIFEST)/deployment.yaml && \
		kubectl apply -f $(TG_BOT_MANIFEST)

.PHONY: apply-vk-bot-manifest
apply-vk-bot-manifest:
	envsubst < $(VK_BOT_MANIFEST)/deployment.yaml && \
		kubectl apply -f $(VK_BOT_MANIFEST)
