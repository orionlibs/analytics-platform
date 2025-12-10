# Main configuration

TEST_OUTPUT ?= ./testoutput
OCI_BIN ?= docker
COMPOSE_ARGS ?= -f docker-compose-java.yml

.DEFAULT_GOAL := all

.PHONY: all
all: integration-test

.PHONY: prepare-integration-test
prepare-integration-test:
	@echo "### Removing resources from previous integration tests, if any"
	rm -rf $(TEST_OUTPUT) || true
	mkdir -p $(TEST_OUTPUT)
	$(MAKE) cleanup-integration-test

.PHONY: cleanup-integration-test
cleanup-integration-test:
	@echo "### Removing integration test Compose cluster"
	$(OCI_BIN) compose $(COMPOSE_ARGS) stop || true
	$(OCI_BIN) compose $(COMPOSE_ARGS) rm -f || true
	$(OCI_BIN) rmi -f $(shell $(OCI_BIN) images --format '{{.Repository}}:{{.Tag}}' | grep 'hatest-') || true

.PHONY: run-integration-test
run-integration-test:
	@echo "### Running integration tests"
	go clean -testcache
	go test -v -timeout 30m -mod vendor -a ./...

.PHONY: integration-test
integration-test: prepare-integration-test
	$(MAKE) run-integration-test || (ret=$$?; $(MAKE) cleanup-integration-test && exit $$ret)
	$(MAKE) cleanup-integration-test
