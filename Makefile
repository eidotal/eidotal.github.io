.PHONY: test

MAKEFILE_ICON = " "
PROJ_NAME = wiki
RUN_ARGS =
WA = $(shell pwd)

define StageInfo
	@echo "--------------------------------- "
	@echo " $(MAKEFILE_ICON) Stage - $(1)"
	@echo "--------------------------------- "
endef


ifndef ASCIIDOCTOR_ARGS
# ASCIIDOCTOR_ARGS = -a relfilesuffix=.html -a docinfodir=${WA}/utils -a docinfo=shared
ASCIIDOCTOR_ARGS = -a relfilesuffix=.html
endif


.PHONY:all
all: Index-html Pages-html

.PHONY:clean
clean:
	rm -rf output/ .vscode/

.PHONY:Index-html
Index-html:
	$(call StageInfo, $@)
	@mkdir -p output/html
	asciidoctor *.adoc $(ASCIIDOCTOR_ARGS) -D output/html

.PHONY:Pages-html
Pages-html:
	$(call StageInfo, $@)
	@mkdir -p output/html/Pages
	cp Pages/DV_ENV.svg output/html/Pages/
	asciidoctor Pages/*.adoc $(ASCIIDOCTOR_ARGS) -D output/html/Pages


.PHONY:open-idex
open-idex:
	$(call StageInfo, $@)
	firefox -new-window output/html/index.html
