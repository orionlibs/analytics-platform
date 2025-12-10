VERSION := $(shell if [ -f version ]; then cat version; else echo "Error: version file not found"; exit 1; fi)  # e.g. v0.11.0
MINOR_VERSION := $(shell echo $(VERSION) | cut -d. -f1,2)  # e.g. v0.11
MAJOR_VERSION := $(shell echo $(VERSION) | cut -d. -f1)  # e.g. v0

.PHONY: release versions

versions:
	@echo sem_var:	$(VERSION)
	@echo minor:		$(MINOR_VERSION)
	@echo major:		$(MAJOR_VERSION)

release:
	git tag -a -m "Release $(VERSION)" $(VERSION)
	git push origin tag $(VERSION)
	gh release create $(VERSION) --generate-notes

	git tag -f $(MINOR_VERSION)
	git push -f origin tag $(MINOR_VERSION)

	git tag -f $(MAJOR_VERSION)
	git push -f origin tag $(MAJOR_VERSION)
