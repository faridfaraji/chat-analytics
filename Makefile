# Project configuration
PROJECT_NAME = chat-analytics
DOCKER_REGISTRY_REPO = northamerica-northeast1-docker.pkg.dev/iron-burner-389219/awesoon

# General Parameters
TOPDIR = $(shell git rev-parse --show-toplevel)
CONDA_SH := $(shell find ~/*conda*/etc -name conda.sh | tail -1)
ACTIVATE := source $(CONDA_SH) && conda activate $(PROJECT_NAME)
ifeq ($(shell uname -p), arm)
DOCKER_PLATFORM = --platform linux/amd64
else
DOCKER_PLATFORM =
endif

default: help

help: # Display help
	@awk -F ':|##' \
		'/^[^\t].+?:.*?##/ {\
			printf "\033[36m%-30s\033[0m %s\n", $$1, $$NF \
		}' $(MAKEFILE_LIST) | sort

run-local: ## run on custom local port. set PORT variable to desired port
	cd $(TOPDIR) && \
	FLASK_APP=template.app \
	flask run --host=0.0.0.0 --no-debugger --no-reload -p $(PORT)

run: ## Run the service with gunicorn
	cd $(TOPDIR) && \
	FLASK_APP=template.app \
	./entrypoint.sh

run-celery: # Run celery workers
	./entrypoint_celery.sh $(NUM_WORKERS)

run-celery-beat: # Run celery beat
	celery -A chat_analytics.celery.tasks beat --loglevel=info

build-docker: ## Build the docker image
	docker build $(DOCKER_PLATFORM) -t $(PROJECT_NAME) .

build-docker-celery: ## Build the docker celery image
	docker build $(DOCKER_PLATFORM) -t $(PROJECT_NAME)-celery -f build/celery/Dockerfile .

build-docker-celery-beat: ## Build the docker celery beat image
	docker build $(DOCKER_PLATFORM) -t $(PROJECT_NAME)-celery-beat -f build/celery_beats/Dockerfile .

tag-docker: ## Tag the docker image
	docker tag $(PROJECT_NAME) $(DOCKER_REGISTRY_REPO)/$(PROJECT_NAME):latest

tag-docker-celery: ## Tag the docker celery image
	docker tag $(PROJECT_NAME)-celery $(DOCKER_REGISTRY_REPO)/$(PROJECT_NAME)-celery:latest

tag-docker-celery-beat: ## Tag the docker celery image
	docker tag $(PROJECT_NAME)-celery-beat $(DOCKER_REGISTRY_REPO)/$(PROJECT_NAME)-celery-beat:latest

push-docker: ## push the image to registry
	docker push $(DOCKER_REGISTRY_REPO)/$(PROJECT_NAME):latest

push-docker-celery: ## push the image to registry
	docker push $(DOCKER_REGISTRY_REPO)/$(PROJECT_NAME)-celery:latest

push-docker-celery-beat: ## push the image to registry
	docker push $(DOCKER_REGISTRY_REPO)/$(PROJECT_NAME)-celery-beat:latest

test: ## Run tox
	tox

clean-code: ## Remove unwanted files in this project (!DESTRUCTIVE!)
	@cd $(TOPDIR) && git clean -ffdx && git reset --hard

clean-docker: ## Remove all docker artifacts for this project (!DESTRUCTIVE!)
	@docker image rm -f $(shell docker image ls --filter reference='$(DOCKER_REPO)' -q) || true

setup: ## Setup the full environment (default)
	conda env update -f environment.yml

setup-mamba: ## Setup the full environment (default)
	mamba env update -f environment.yml

release-publish: ## push release to git after git flow release publish
	git checkout main
	git push
	git checkout develop
	git push
	git push --tags

docker-build: ## builds docker image
	@echo "note platform specified for compatibility when building on apple silicon"
	@echo $(DOCKER_PLATFORM)
	docker build --build-arg GIT_TOKEN=$(GIT_TOKEN)  --build-arg AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) --build-arg AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) $(DOCKER_PLATFORM) -t awesoon/$(PROJECT_NAME) .

docker-tag-dev: ## tag the docker image for ecr repo dev
	docker tag awesoon/$(PROJECT_NAME):latest aws_ecr_url/awesoon/$(PROJECT_NAME):latest

docker-tag-prod: ## tag the docker image for ecr repo prod (to be changed)
	docker tag awesoon/$(PROJECT_NAME):latest aws_ecr_url/awesoon/$(PROJECT_NAME):latest

docker-push: ## aws docker login + pushes docker image to AWS ECR
	@echo "attempting to docker login for AWS..."
	@echo "note this uses your default aws-cli profile unless you specify otherwise"
	@echo "for example, if you want to use a profile called prod: make docker-push ARGS=\"--profile=prod\""
	aws $(ARGS) ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 383620305052.dkr.ecr.us-east-1.amazonaws.com/awesoon/$(PROJECT_NAME)
	docker push aws_ecr_url/awesoon/$(PROJECT_NAME):latest

.PHONY: default debug help start start-dev build-docker run-docker stop-docker test clean-code clean-docker code setup release-publish
