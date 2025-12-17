# Document name (without extension)
DOCUMENT = Report

LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error
BIBER = biber
VIEWER = evince

TEX_SOURCES := $(wildcard *.tex chapters/*.tex appendices/*.tex \
                prefrontmatter/*.tex frontmatter/*.tex preamble/*.tex)
BIB_SOURCES := $(wildcard bibliography/*.bib)

.PHONY: all clean distclean view quick help

all: clean $(DOCUMENT).pdf

$(DOCUMENT).pdf: $(TEX_SOURCES) $(BIB_SOURCES)
	@echo "First LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex
	@echo "Running Biber..."
	$(BIBER) $(DOCUMENT)
	@echo "Second LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex
	@echo "Third LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex
	@echo "Document compiled successfully!"

clean:
	@echo "Cleaning auxiliary files..."
	@rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.bcf *.run.xml *.synctex.gz
	@rm -f chapters/*.aux appendices/*.aux prefrontmatter/*.aux frontmatter/*.aux
	@rm -f *.acn *.acr *.alg *.glg *.glo
	@echo "Clean complete!"

distclean: clean
	@rm -f $(DOCUMENT).pdf

view: $(DOCUMENT).pdf
	$(VIEWER) $(DOCUMENT).pdf &

quick:
	@echo "Quick compile..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex

help:
	@echo "Targets:"
	@echo "  make        - Incremental build"
	@echo "  make all    - Clean + full build"
	@echo "  make clean  - Remove auxiliary files"
	@echo "  make distclean - Remove aux files and PDF"
	@echo "  make view   - Open the PDF"
	@echo "  make quick  - Single-pass compile"

