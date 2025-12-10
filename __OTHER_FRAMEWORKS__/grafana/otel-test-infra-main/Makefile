# Main configuration
GOOS ?= linux
GOARCH ?= amd64

.DEFAULT_GOAL := all

# go-install-tool will 'go install' any package $2 and install it locally to $1.
# This will prevent that they are installed in the $USER/go/bin folder and different
# projects ca have different versions of the tools
PROJECT_DIR := $(shell dirname $(abspath $(firstword $(MAKEFILE_LIST))))

TOOLS_DIR ?= $(PROJECT_DIR)/bin

define go-install-tool
@[ -f $(1) ] || { \
set -e ;\
TMP_DIR=$$(mktemp -d) ;\
cd $$TMP_DIR ;\
go mod init tmp ;\
echo "Downloading $(2)" ;\
GOBIN=$(TOOLS_DIR) GOFLAGS="-mod=mod" go install $(2) ;\
rm -rf $$TMP_DIR ;\
}
endef

# Check that given variables are set and all have non-empty values,
# die with an error otherwise.
#
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))

# prereqs binary dependencies
GOLANGCI_LINT = $(TOOLS_DIR)/golangci-lint
GOIMPORTS_REVISER = $(TOOLS_DIR)/goimports-reviser
GO_LICENSES = $(TOOLS_DIR)/go-licenses
define check_format
	$(shell $(foreach FILE, $(shell find . -name "*.go" -not -path "./vendor/*"), \
		$(GOIMPORTS_REVISER) -local github.com/grafana -list-diff -output stdout -file-path $(FILE);))
endef

.PHONY: prereqs
prereqs:
	@echo "### Check if prerequisites are met, and installing missing dependencies"
	$(call go-install-tool,$(GOLANGCI_LINT),github.com/golangci/golangci-lint/cmd/golangci-lint@v1.52.2)
	$(call go-install-tool,$(GOIMPORTS_REVISER),github.com/incu6us/goimports-reviser/v2@v2.5.3)
	$(call go-install-tool,$(GO_LICENSES),github.com/google/go-licenses@v1.6.0)

.PHONY: fmt
fmt:
	@echo "### Formatting code and fixing imports"
	@$(foreach FILE, $(shell find . -name "*.go" -not -path "./vendor/*"), \
		$(GOIMPORTS_REVISER) -local github.com/grafana -file-path $(FILE);)

.PHONY: checkfmt
checkfmt:
	@echo '### check correct formatting and imports'
	@if [ "$(strip $(check_format))" != "" ]; then \
		echo "$(check_format)"; \
		echo "Above files are not properly formatted. Run 'make fmt' to fix them"; \
		exit 1; \
	fi

.PHONY: lint
lint: checkfmt
	@echo "### Linting code"
	$(GOLANGCI_LINT) run ./... --timeout=3m

.PHONY: verify
verify: prereqs lint

.PHONY: all
all: verify

.PHONY: update-licenses
update-licenses: prereqs
	@echo "### Updating third_party_licenses.csv"
	$(GO_LICENSES) report --include_tests ./... > third_party_licenses.csv