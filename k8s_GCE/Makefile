PROJECT_DIR = cryptostock_api
BE_CODE_DIR = cryptostock
NOTIFICATION_SERVICES_DIR = cryptostock_notification_services
UI_APP_PATH = ui/cryptostock_app/

# gcloud config get-value project
GCE_PROJECT_ID = maximal-valve-352911
LOCATION = us-central1
COMPUTE_ZONE = "${LOCATION}-c"
REPO_NAME = cryptostock-repo
CLUSTER_NAME = cryptostock-cluster
NODES_COUNT = 1

STAGE = dev
BE_BUILD_TAG = 1.0.0
UI_BUILD_TAG = 1.0.0
NOTIFICATION_BOTS_IMAGE_TAG = 1.0.0

DB_MANIFEST = ../k8s/postgres
BE_MANIFEST = ../k8s/be_django
REDIS_MANIFEST = ../k8s/redis
CELERY_MANIFEST = ../k8s/celery
TG_BOT_MANIFEST = ../k8s/tg_bot
VK_BOT_MANIFEST = ../k8s/vk_bot
UI_MANIFEST = ../k8s/fe_react

export DNS=cryptostock.market.sample
export BE_IMAGE_NAME="$(LOCATION)-docker.pkg.dev/$(GCE_PROJECT_ID)/$(REPO_NAME)/be-${STAGE}:${BE_BUILD_TAG}"
export NOTIFICATION_BOTS_IMAGE_NAME="$(LOCATION)-docker.pkg.dev/$(GCE_PROJECT_ID)/$(REPO_NAME)/ns-${STAGE}:${NOTIFICATION_BOTS_IMAGE_TAG}"
export NODE_IP=34.136.241.70
export APP_PORT=8543
export UI_BUILDER_NAME="$(LOCATION)-docker.pkg.dev/$(GCE_PROJECT_ID)/$(REPO_NAME)/fe-build:latest"
export UI_IMAGE_NAME="$(LOCATION)-docker.pkg.dev/$(GCE_PROJECT_ID)/$(REPO_NAME)/ui-${STAGE}:${UI_BUILD_TAG}"
export REACT_APP_BASE_URL="http://${DNS}/api/"

all: | export-requirements-app be-build export-requirements-notification-services \
	   notification-services-build create-ui-builder ui-build


.PHONY: test
test:
	echo $$UI_BUILDER_NAME
	echo $$UI_IMAGE_NAME
# create repo in gce special for project
.PHONY: create-gce-repo
create-gce-repo:
	gcloud artifacts repositories create $(REPO_NAME) \
	--project=$(GCE_PROJECT_ID) \
    --repository-format=docker \
    --location=$(LOCATION) \
    --description="Docker repository for cryptostock"

.PHONY: create-gce-cluster
create-gce-cluster:
	gcloud container clusters create $(CLUSTER_NAME) \
    --num-nodes $(NODES_COUNT) \
    --zone $(COMPUTE_ZONE)

.PHONY: export-requirements-app
export-requirements-app:
	cd ../$(PROJECT_DIR) && \
	poetry export -f requirements.txt --output requirements.txt --dev --without-hashes && \
	mv requirements.txt $(BE_CODE_DIR)/

.PHONY: be-build
be-build:
	cd ../$(PROJECT_DIR)/$(BE_CODE_DIR) && \
	gcloud builds submit --tag $(BE_IMAGE_NAME) .

.PHONY: export-requirements-notification-services
export-requirements-notification-services:
	cd ../$(NOTIFICATION_SERVICES_DIR) && \
	poetry export -f requirements.txt --output requirements.txt --dev --without-hashes

.PHONY: notification-services-build
notification-services-build:
	cd ../$(NOTIFICATION_SERVICES_DIR) && \
	gcloud builds submit --tag $(NOTIFICATION_BOTS_IMAGE_NAME) .

.PHONY: create-ui-builder
create-ui-builder:
	gcloud builds submit --config ui-builder-cloudbuild.yaml "../$(UI_APP_PATH)." \
	--substitutions=_UI_BUILDER_NAME=$(UI_BUILDER_NAME),_REACT_APP_BASE_URL=$(REACT_APP_BASE_URL)

.PHONY: ui-build
ui-build:
	gcloud builds submit --config ui-image-cloudbuild.yaml "$(UI_MANIFEST)." \
	--substitutions=_UI_BUILDER_NAME=$(UI_BUILDER_NAME),_UI_IMAGE_NAME=$(UI_IMAGE_NAME)
