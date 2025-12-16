# Makefile for compiling LaTeX document with XeLaTeX and Biber
# Usage:
#   make        - Compile the document
#   make clean  - Remove auxiliary files
#   make view   - Open the PDF (Linux)
#   make all    - Clean and compile

# Document name (without extension)
DOCUMENT = Report

# LaTeX compiler
LATEX = xelatex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

# Bibliography compiler
BIBER = biber

# PDF viewer (adjust for your system)
VIEWER = xdg-open

# Main target
.PHONY: all
all: clean $(DOCUMENT).pdf

# Compile the document
$(DOCUMENT).pdf: $(DOCUMENT).tex
	@echo "First LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex
	@echo "Running Biber..."
	$(BIBER) $(DOCUMENT)
	@echo "Second LaTeX pass..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex
	@echo "Third LaTeX pass (resolving references)..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex
	@echo "Document compiled successfully!"

# Clean auxiliary files
.PHONY: clean
clean:
	@echo "Cleaning auxiliary files..."
	@rm -f $(DOCUMENT).aux $(DOCUMENT).bbl $(DOCUMENT).bcf $(DOCUMENT).blg \
	       $(DOCUMENT).log $(DOCUMENT).out $(DOCUMENT).run.xml $(DOCUMENT).toc \
	       $(DOCUMENT).lof $(DOCUMENT).lot
	@rm -f chapters/*.aux appendices/*.aux prefrontmatter/*.aux frontmatter/*.aux
	@echo "Clean complete!"

# Deep clean (including PDF)
.PHONY: distclean
distclean: clean
	@echo "Removing PDF..."
	@rm -f $(DOCUMENT).pdf
	@echo "Deep clean complete!"

# View the PDF
.PHONY: view
view: $(DOCUMENT).pdf
	$(VIEWER) $(DOCUMENT).pdf &

# Force recompile
.PHONY: force
force: clean all

# Quick compile (single pass, for drafts)
.PHONY: quick
quick:
	@echo "Quick compile (single pass)..."
	$(LATEX) $(LATEX_FLAGS) $(DOCUMENT).tex
	@echo "Quick compile complete!"

# Help message
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make          - Compile the document (default)"
	@echo "  make all      - Clean and compile"
	@echo "  make clean    - Remove auxiliary files"
	@echo "  make distclean - Remove auxiliary files and PDF"
	@echo "  make view     - Open the PDF"
	@echo "  make force    - Force recompile from scratch"
	@echo "  make quick    - Quick single-pass compile (draft mode)"
	@echo "  make help     - Show this help message"
