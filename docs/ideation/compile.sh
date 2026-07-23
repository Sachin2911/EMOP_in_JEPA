#!/usr/bin/env bash
# Compile the ideation document (Wits CSAM report template).
# All LaTeX sources live in ./latex; intermediate files stay in ./latex/build;
# the final PDF lands here as ./ID.pdf.
#
# Usage:
#   ./compile.sh          build the PDF
#   ./compile.sh clean    remove the build directory and the compiled PDF
set -euo pipefail

DOC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LATEX_DIR="$DOC_DIR/latex"
BUILD_DIR="$LATEX_DIR/build"
OUT_PDF="$DOC_DIR/ID.pdf"

if [[ "${1:-}" == "clean" ]]; then
    rm -rf "$BUILD_DIR" "$OUT_PDF"
    echo "Cleaned build artifacts."
    exit 0
fi

mkdir -p "$BUILD_DIR"
cd "$LATEX_DIR"

pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" main.tex

# BibTeX must run inside build/ (openout_any blocks writes via absolute paths)
(
  cd "$BUILD_DIR"
  export BIBINPUTS="${LATEX_DIR}:."
  export BSTINPUTS="${LATEX_DIR}:."
  bibtex main
)

pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" main.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$BUILD_DIR" main.tex

cp "$BUILD_DIR/main.pdf" "$OUT_PDF"
echo "PDF written to $OUT_PDF"
