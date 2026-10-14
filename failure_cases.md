# Failure Cases and Improvements

## Known failure cases
1. **Relative dates:** “yesterday” is not converted to a calendar date because no trusted incident timestamp is supplied.
2. **Ambiguous date formats:** `03/04/2026` may mean 3 April or March 4 depending on locale; the baseline cannot safely disambiguate it.
3. **Non-date contradictions:** The baseline currently checks date conflicts, not all fields such as location, vehicle identifier, or damage amount.
4. **Document status:** Text such as “I have photos” is treated as a document mention, but the app cannot verify whether a file is attached or legible.
5. **Classification coverage:** Rule-based keywords can miss uncommon claim types or misclassify text containing several topics.
6. **Field extraction:** Names, locations, policy identifiers, and vehicle registrations may be missed if phrased unusually.
7. **No OCR or email ingestion:** Uploaded claim forms and attachments are not parsed.
8. **No external AI call:** This is a transparent baseline, not a production-grade LLM system.

## Improvements
- Add source-level field extraction and conflict checks for all important fields.
- Require an evidence quote and source label for every extracted field.
- Use schema-constrained model output only as a candidate; validate it with deterministic checks.
- Add OCR and file upload handling with safe file-type restrictions.
- Expand labelled test data and evaluate precision, recall, F1, JSON validity, and unsupported-value rate.
- Add human review and audit logs before integration with claim-management systems.
- Never use the tool to decide claim liability, fraud, coverage, or payout automatically.
