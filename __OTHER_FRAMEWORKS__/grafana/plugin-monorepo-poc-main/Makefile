.PHONY: .drone.jsonnet

plugins := $(shell ls ./plugins)

.drone.jsonnet: ## Render .drone.yml pipeline file
	drone jsonnet --extVar "plugins=$(plugins)" --stream --format --source .drone/drone.jsonnet --target .drone.yml
	drone lint .drone.yml
