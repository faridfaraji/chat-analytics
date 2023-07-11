# Project configuration
PROJECT_NAME = template

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
