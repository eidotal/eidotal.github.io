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
ASCIIDOCTOR_ARGS = -a relfilesuffix=.html -a project-root=${WA} -a docinfodir=${WA}/utils/docinfo-local -a docinfo=shared
# ASCIIDOCTOR_ARGS = -a relfilesuffix=.html
endif

ifndef ASCIIDOCTOR_REMOTE_ARGS
ASCIIDOCTOR_REMOTE_ARGS = -a relfilesuffix=.html -a project-root=${WA} -a docinfodir=${WA}/utils/docinfo -a docinfo=shared
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
	@mkdir -p output/html/Pages/About
	@mkdir -p output/html/Pages/Network
	@mkdir -p output/html/Pages/Workflow
	@mkdir -p output/html/Pages/svDV
	cp Pages/svDV/DV_ENV.svg output/html/Pages/svDV
	cp Pages/Network/PG.svg  output/html/Pages/Network
	cp Pages/Network/PPC.svg  output/html/Pages/Network
	cp Pages/Network/PPC.png  output/html/Pages/Network
	cp Pages/Network/pktlib-sim.html output/html/Pages/Network
	asciidoctor Pages/About/*.adoc $(ASCIIDOCTOR_ARGS) -D output/html/Pages/About
	asciidoctor Pages/Network/*.adoc $(ASCIIDOCTOR_ARGS) -D output/html/Pages/Network
	asciidoctor Pages/Workflow/*.adoc $(ASCIIDOCTOR_ARGS) -D output/html/Pages/Workflow
	asciidoctor Pages/svDV/*.adoc $(ASCIIDOCTOR_ARGS) -D output/html/Pages/svDV

.PHONY:Diagram
Diagram:
	$(call StageInfo, $@)
	@mkdir -p output/html/Pages/Network
	mmdc -i Pages/Network/ParseGraph.mmd -o output/html/Pages/Network/PG.mmd.svg
	d2 Pages/Network/ParseGraph.d2 output/html/Pages/Network/PG.d2.svg

.PHONY:PDF
PDF:
	$(call StageInfo, $@)
	@mkdir -p output/pdf
	@mkdir -p output/pdf/Pages/About
	@mkdir -p output/pdf/Pages/Network
	@mkdir -p output/pdf/Pages/Workflow
	@mkdir -p output/pdf/Pages/svDV
	cp Pages/svDV/DV_ENV.svg output/pdf/Pages/svDV
	cp Pages/Network/PG.svg output/pdf/Pages/Network
	asciidoctor-pdf *.adoc $(ASCIIDOCTOR_ARGS) -D output/pdf
	asciidoctor-pdf Pages/About/*.adoc $(ASCIIDOCTOR_ARGS) -D output/pdf/Pages/About
	asciidoctor-pdf Pages/Network/*.adoc $(ASCIIDOCTOR_ARGS) -D output/pdf/Pages/Network
	asciidoctor-pdf Pages/Workflow/*.adoc $(ASCIIDOCTOR_ARGS) -D output/pdf/Pages/Workflow
	asciidoctor-pdf Pages/svDV/*.adoc $(ASCIIDOCTOR_ARGS) -D output/pdf/Pages/svDV


.PHONY:open
open:
	$(call StageInfo, $@)
	firefox -new-window output/html/index.html

# --------------------------------------------------------
ifndef INSTALL_CMD
INSTALL_CMD = apt-get install -y
endif

.PHONY: install
install:
	sudo $(INSTALL_CMD) asciidoctor gem
	sudo gem install pygments.rb

.PHONY: create
create:
	asciidoctor index.adoc
	asciidoctor Pages/*/*.adoc $(ASCIIDOCTOR_REMOTE_ARGS)
