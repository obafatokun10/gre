#!/usr/bin/env bash
# Rebuild the app from the ETS PDF. Usage: tools/rebuild.sh path/to/book.pdf
# Needs poppler-utils (pdftotext, pdftoppm) and Python 3 with Pillow and NumPy.
set -euo pipefail
PDF="$1"
cd "$(dirname "$0")/.."
mkdir -p build/pages
pdftotext -bbox-layout -f 58 -l 219 "$PDF" build/bbox.html
python3 tools/parse.py build/bbox.html build/regions.json > build/parse.log
pdftoppm -r 180 -png -f 63 -l 220 "$PDF" build/pages/p
python3 tools/crop.py build/pages build/regions.json build/img
python3 tools/key.py build/img/sizes.json tools/questions.json build/img
python3 tools/pack.py build/img img
python3 tools/build.py tools/template.html tools/questions.json index.html
