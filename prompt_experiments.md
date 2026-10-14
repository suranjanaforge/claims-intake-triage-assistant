# Prompt Experiments

The current app is a deterministic baseline and does not call an LLM. These prompt experiments describe how a future LLM-backed extractor should be evaluated. Keep rule-based validation after any model output.

## Experiment 1 — Direct extraction
**Prompt:** Extract only explicitly stated facts from the claim text. Return JSON with claim type, incident type, incident date, time, location, policy number, asset identifier, damage/loss, and document mentions. Use `null` for missing fields. Do not infer facts.

**Expected risk:** A model may fill gaps with plausible but unsupported values.

## Experiment 2 — Evidence-grounded extraction
**Prompt:** For every extracted field, include the exact supporting quote and source label. If no quote supports a value, return null. Do not treat a document being mentioned as proof it was attached or reviewed.

**Expected improvement:** Easier auditing and less unsupported extraction.

## Experiment 3 — Multi-source conflict detection
**Prompt:** Extract candidate values separately by source. If two sources provide different values for the same field, preserve both values, flag a conflict, and do not select a winner. Ask for clarification as a next step.

**Expected improvement:** Reduces silent resolution of contradictions.

## Evaluation plan
Compare all experiments against the same 20 synthetic claims. Measure:
- Claim type accuracy on labelled examples.
- Required-field extraction precision/recall on explicitly stated values.
- Missing-field detection accuracy.
- Conflict detection recall.
- Unsupported-value rate (target: 0).
- Valid JSON rate.

No LLM experiment results are claimed here because no external model was called. Run `python evaluate.py` for the deterministic baseline smoke tests.
