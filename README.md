# claims-intake-triage-assistant
# Claims Intake & Triage Assistant

A small Streamlit demonstration that converts unstructured, **synthetic** claim descriptions into a structured record, identifies missing information, flags conflicting incident dates, assigns an initial triage category, and recommends next steps.

## Features
- Claim-type and incident-type classification using a transparent baseline.
- Extraction of explicitly stated policy number, dates, time, location, claimant name, and vehicle registration where recognizable.
- Supporting-document mentions (a mention is not treated as proof that a file was reviewed).
- Missing-field checklist.
- Source-labelled contradiction detection for dates.
- JSON output download.
- Clear distinction between claimant-provided information and system inferences/recommendations.
- 20 synthetic test cases and a reproducible evaluation script.

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Use
Paste a synthetic claim description in the app and click **Analyze claim**. For contradictions, label sources explicitly, for example:

```text
Claim form: Accident date = 12 Sept 2026. Policy number: POL-2048.
Email: Accident date = 13 Sept 2026. Photos available.
```

The app should flag the dates rather than silently choosing one.

## Project structure
- `app.py` — Streamlit application and extraction baseline.
- `sample_claims.json` — 20 synthetic test claims with expected properties.
- `evaluate.py` — runs the test cases and reports basic metrics.
- `input_output_schema.json` — input and output schema reference.
- `prompt_experiments.md` — prompt design and experiment notes for a future LLM-backed version.
- `evaluation_results.json` — baseline evaluation results from `evaluate.py`.
- `failure_cases.md` — limitations and improvement plan.

## Evaluation
Run:

```bash
python evaluate.py
```

The test suite checks broad claim-type detection and whether known contradictory dates are flagged. It is a small smoke-test suite, not a statistically representative benchmark. See `evaluation_results.json` for the measured result.

## Design choices and limitations
This initial version uses deterministic Python rules rather than a live LLM API, so it runs without an API key and produces reproducible results. Its extraction coverage is limited; dates in ambiguous formats, implicit details, synonyms, and multi-source inconsistencies other than dates may be missed. It should not be used for automated claim approval, denial, fraud accusations, liability determination, or coverage decisions. A human claims professional must review outputs.

## Privacy and responsible use
- Use only synthetic or public data in this repository.
- Do not commit customer names, policy numbers, medical records, claim documents, or other personal data.
- The triage label is an intake workflow suggestion, not a decision about eligibility, liability, or payment.
- The system must not invent missing values. Missing values are represented as `null` or listed under `missing_information`.
- Source text and system-generated classifications/recommendations are labelled separately.

## AI usage disclosure
AI assistance was used to help design and draft the application, documentation, synthetic test cases, schema, and evaluation scaffolding. The submitted implementation uses transparent rule-based extraction and validation rather than calling an external generative AI service. All claim examples are synthetic.
