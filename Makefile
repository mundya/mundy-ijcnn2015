# Simple Xe/LaTeX Makefile
# (C) Andrew Mundy 2012

# Configuration
TEX=pdflatex
BIB=bibtex
TEXFLAGS=--shell-escape
BIBFLAGS=
texdoc=ijcnn-mundy

.PHONY: clean
.PHONY: biber
.PHONY: complete

# Make all items
all : $(texdoc).tex
	$(TEX) $(TEXFLAGS) $(texdoc)

# Complete (rather than quick build)
complete : clean bib all

# Generate reference requirements
$(texdoc).aux :
	$(TEX) $(TEXFLAGS) $(texdoc)

# Generate the bibliography
bib : all
	$(BIB) $(BIBFLAGS) $(texdoc)
	$(TEX) $(TEXFLAGS) $(texdoc)
	$(TEX) $(TEXFLAGS) $(texdoc)

# Clean
clean :
	find . -type f -regex ".*\.\(aux\|bbl\|bcf\|blg\|log\|pdf\|png\|out\|toc\|lof\|lot\|count\)" -delete
