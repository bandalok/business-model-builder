[![CI](https://github.com/bandalok/business-model-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/bandalok/business-model-builder/actions/workflows/ci.yml)

# Business Model Builder

A tool for product managers: fill in the nine blocks of the Business Model
Canvas with guided questions, get a blunt investor-style critique of your
answers, and check whether the unit economics actually work.

Everything runs locally. No API keys, no accounts, no network calls. The
critique engine is rule-based: it rewards specific numbers and named
customers, penalizes vague filler, and cross-checks that the blocks agree
with each other (does your value prop name your segment? do your channels
reach them?).

## Who it is for

Product managers and founders who want a fast, honest gut-check on a
business model before writing a plan or a pitch.

## Features

- **Builder**: a step-by-step wizard, one canvas block at a time, each with
  2-3 plain-English guided questions. Progress is saved in your browser.
- **Canvas**: the classic 9-block grid, rendered from your answers.
- **Critique**: an overall score out of 100, per-block scores, a list of
  strengths, and investor questions about the weak spots.
- **Economics**: a unit economics calculator with live results — revenue,
  gross margin, break-even customers, LTV, LTV:CAC, and CAC payback.
- **SampleCo**: a realistic fictional B2B SaaS example preloaded, so the
  demo is useful the moment you open it.

## Try it

Live demo: https://bandalok.github.io/business-model-builder/

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pytest
```

No third-party dependencies. Python 3.9 or newer.

Use it from Python:

```python
from bmc import critique_model, calculate_economics, SAMPLE_MODEL, SAMPLE_ECONOMICS

result = critique_model(SAMPLE_MODEL)
print(result["overall_score"])   # 70
print(result["risks"])           # investor questions, if any

econ = calculate_economics(**SAMPLE_ECONOMICS)
print(econ["ltv_cac_ratio"])     # 20.07
```

## Sample walkthrough

1. Open the demo. SampleCo (team analytics SaaS, $49/seat/month) is preloaded.
2. Go to **Critique**. It scores 70/100 with concrete strengths and no red
   flags — a healthy example.
3. Delete the price from Revenue Streams and run the critique again. Watch
   the score drop and the investor questions appear.
4. Go to **Economics**. Change the customer count and see break-even move.

## Project layout

```
bmc/blocks.py          the 9 canvas blocks, guided questions, hints
bmc/critique.py        rule-based critique engine (no AI calls)
bmc/unit_economics.py  pure-function unit economics calculator
bmc/sample.py          SampleCo fixture used by tests and the demo
tests/                 pytest suite
docs/index.html        self-contained web demo (GitHub Pages ready)
```

## License

MIT License, (c) 2026 Alok Band. See LICENSE.
