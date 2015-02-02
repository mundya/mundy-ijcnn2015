# Simple Xe/LaTeX Makefile
# (C) Andrew Mundy 2012

# Configuration
TEX=pdflatex
BIB=bibtex
TEXFLAGS=--shell-escape
BIBFLAGS=
texdoc=apt_presentation

.PHONY: clean
.PHONY: bib
.PHONY: algorithm_diagram

# Make all items
all : $(texdoc).tex
	$(TEX) $(TEXFLAGS) $(texdoc)

# Generate reference requirements
$(texdoc).aux :
	$(TEX) $(TEXFLAGS) $(texdoc)

# Generate the bibliography
bib : $(texdoc).aux
	$(BIB) $(BIBFLAGS) $(texdoc)
	$(TEX) $(TEXFLAGS) $(texdoc)
	$(TEX) $(TEXFLAGS) $(texdoc)

algorithm_diagram : algorithm_diagram.tex
	$(TEX) algorithm_diagram.tex
	$(TEX) algorithm_diagram.tex

# Clean
clean :
	rm $(texdoc).pdf
