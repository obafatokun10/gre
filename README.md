# GRE Quant Practice

A practice app for the 150 questions in *Official GRE Quantitative Reasoning Practice Questions, Volume 1* (ETS). It is for personal study only. The questions and explanations are © ETS, so keep this repository private.

## What it does

- **7 sets:** Arithmetic (19), Algebra (17), Geometry (13), Data Analysis (26) and Mixed Practice Sets 1–3 (25 each).
- **Practice mode:** answer, check, then read the book's explanation. A per-question timer shows your pace; about 1:45 is the target.
- **Timed test mode:** a countdown of about 1¾ minutes per question, with no feedback until you submit. You then get a score by question type and a review of every question.
- **Drills across all sets:** by question type, questions you haven't tried, questions you missed, or questions you marked.
- **A GRE-style calculator** with "Transfer display" into the numeric answer box.
- **Fraction answers** accept equivalent fractions, as on the real test.
- **Keyboard:** A–H selects an answer, Enter checks it, and ← / → move between questions.
- **Progress** is saved in the browser's local storage.

Questions and explanations are shown as images cropped from the book, so the maths and figures appear exactly as printed. All 150 answer keys were checked against the book's explanations.

## Running it

`index.html` loads the question images from `img/*.json`, so it must be served over HTTP. Opening the file directly with `file://` won't work. For example:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

GitHub Pages also works. Serving Pages from a private repository needs a paid GitHub plan.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The app: one page with the answer key inlined |
| `img/<set>.json` | Question, explanation and data-set images for each set, as base64 PNG data URIs |
| `tools/template.html` | Source of `index.html`; `/*DATA*/` is replaced with `tools/questions.json` |
| `tools/questions.json` | Answer key: question type, number of choices, correct answer, image sizes, data-set groups |
| `tools/parse.py` | Finds each question and explanation in the PDF's text layout |
| `tools/crop.py` | Crops the rendered pages into question, explanation and data images |
| `tools/key.py` | Builds `questions.json` from the answer key in the script |
| `tools/pack.py` | Packs the PNGs into `img/<set>.json` |
| `tools/rebuild.sh` | Runs the whole pipeline |

## Rebuilding from the PDF

The PDF is not in the repository. With poppler-utils, Python 3, Pillow and NumPy installed, run:

```sh
tools/rebuild.sh path/to/ETS_Official_GRE_Quantitative_Reasoning_Practice_Questions_Vol_1.pdf
```

To change only the app's look or behaviour, edit `tools/template.html` and run:

```sh
python3 tools/build.py tools/template.html tools/questions.json index.html
```
