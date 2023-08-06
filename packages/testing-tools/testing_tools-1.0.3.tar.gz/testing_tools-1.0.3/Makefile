-include ./devops/makefiles/Makefile


test-all:  ## Run all tests
	@$(MAKE) ${MAKE_TAG} echo-cyan msg="2.1. Unit tests"
	@$(MAKE) ${MAKE_TAG} pytest mark=ut

	@$(MAKE) ${MAKE_TAG} echo-cyan msg="2.2. End-to-end tests"
	@$(MAKE) ${MAKE_TAG} pytest mark=e2e
.PHONY: test-all
