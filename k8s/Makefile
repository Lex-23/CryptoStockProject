PROJECT_DIR = cryptostock_api
BE_CODE_DIR = cryptostock
BE_DOCKERFILE_NAME = Dockerfile-k8s
BE_IMAGE_NAME = be-dev:alfa
NAMESPACE_FILE_NAME = dev-namespace.yaml
CONFIGMAP_FILE_NAME = dev-configmap.yaml
BD_MANIFEST = postgres/
CMD = $(minikube docker-env)

all: | start-minikube export-requirements-app be-build apply-namespace \
	   apply-configmap apply-bd-manifest

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

.PHONY: apply-bd-manifest
apply-bd-manifest:
	kubectl apply -f $(BD_MANIFEST)
