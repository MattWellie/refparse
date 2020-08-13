DEFAULT_PDFLATEX=embix/pdflatex
DEFAULT_PDFLATEX_VERSION=v1
DEFAULT_REFPARSE_NAME=refparse:local
target_file:=

# these are the commands which require calling through from shell
UID = $(shell id -u)
GID = $(shell id -g)
current_dir = $(shell pwd)

# dud target - runs help then escapes
.PHONY: description

description:	## show help message, this awk code stolen from Allan Callaghan
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2 } END{print ""}' $(MAKEFILE_LIST)

help: .refparse_built	## run this to see additional command line arguments for the typesetter - this file might not let you use them, but you'll be able to see them...
		docker run $(DEFAULT_REFPARSE_NAME) -h

pdf: .refparse_built tex_generated	## generate a pdf based on the target file (include input/ in the path) - tidies up temp files
	for file in $(shell ls output/*.tex); \
	do docker run --rm --user $(UID):$(GID) -v $(current_dir):/sources embix/pdflatex:v1 -output-directory=output $$file; \
	done
	-mkdir -p output/pdf
	-mkdir -p output/tex
	mv output/*.pdf output/pdf/.
	mv output/*.tex output/tex/.
	-rm output/*.log output/*.upb output/*.upa output/*.out output/*.aux

text: .refparse_built	## generates a text-only transcription from the target_file
	docker run -v $(current_dir)/input:/input -v $(current_dir)/output:/output $(DEFAULT_REFPARSE_NAME) -i $(target_file) --text
	-mkdir -p output/txt
	mv output/*.txt output/txt/.

tex_generated: .refparse_built	## generates a tex file based on the input file target_file
	docker run -v $(current_dir)/input:/input -v $(current_dir)/output:/output $(DEFAULT_REFPARSE_NAME) -i $(target_file)

.pdf_tex_pulled:	## only relevant if tex needs to be translated
	docker pull $(DEFAULT_PDFLATEX):$(DEFAULT_PDFLATEX_VERSION)
	touch $@

.refparse_built: Dockerfile refparse/*	## creates the docker images for use locally
	docker build -t $(DEFAULT_REFPARSE_NAME) .
	touch $@
