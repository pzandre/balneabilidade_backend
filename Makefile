.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help
HEAD = 1

up: ## Run docker compose up as daemon
	docker compose up

makemigrations:  ## Run the makemigrations inside the container
	docker compose run --rm web python3 manage.py makemigrations $(app)

migrate: ## Run the migrate inside the container
	docker compose run --rm web python3 manage.py migrate $(app) $(migration)

flush: ## Run the flush inside the container
	docker compose run --rm web python3 manage.py flush

createsuperuser: ## Run the createsuperuser inside the container
	docker compose run --rm web python3 manage.py createsuperuser

build: ## Build the container
	docker compose build

down:
	docker compose down

shell: ## Run Django shell inside the API container
	docker compose run --rm web python3 manage.py shell

showmigrations: ## Run the showmigrations inside the container
	docker compose run --rm web python3 manage.py showmigrations

flush_cache: ## Run the flush_cache inside the container
	docker compose run --rm web python3 manage.py flush_cache
