# Codex Gap Report

**Date:** March 15, 2026

**Prepared by:** Codex

## Scope

This report describes the current gaps in the alternative Codex implementation:
- code path: `baseline-solution/src/codex_extract_fields.py`
- pipeline: `baseline-solution/src/pipeline_codex.py`
- output workbook: `baseline-solution/output/generated-database-codex.xlsx`

The goal is not to restate what already works. The goal is to describe what is still missing in necessary and sufficient detail so the next step can be chosen cleanly.

## Current State

The Codex implementation is materially better than the earlier Gemini workbook on raw coverage:
- workbook shape: `50 x 88`
- non-empty generated cells: `661`
- best normalized match against the populated prototype row: `10/12`

It also preserves the clinician-facing workbook styling by writing through the prototype template.

That said, the implementation is still incomplete. Most of the remaining problems are extraction-coverage problems, not presentation problems.

## Primary Gaps

### 1. Large parts of the target schema are still unimplemented

The Codex workbook leaves 61 columns completely empty.

Important examples:
- `Endoscopy: date(f)`
- `Histology: Biopsy date(g)`
- all chemotherapy fields
- all immunotherapy fields
- all radiotherapy fields
- all CEA fields
- all surgery fields
- all second-MRI fields
- all 12-week MRI fields
- flexi-sig follow-up fields
- watch-and-wait follow-up date fields

This means the current parser is still a first-pass extractor for baseline demographics, diagnosis, selected endoscopy fields, selected CT/MRI staging, and one MDT decision field. It is not yet a broad schema implementation.

### 2. Endoscopy date extraction is missing entirely

`Endoscopy: date(f)` is empty for all 50 rows.

This is a real gap, not just missing source data. The source document contains endoscopy mentions such as:
- `Colonoscopy : ...`
- `Colonoscopy: ...`
- `Flexi sig 20/10/2024: ...`

The current extractor only captures type and findings when it sees an endoscopy phrase, but it does not reliably promote associated dates into the target date field.

### 3. Histology biopsy date extraction is missing entirely

`Histology: Biopsy date(g)` is empty for all 50 rows.

The current implementation only looks for explicit biopsy-date phrasing, which is too narrow. In practice, histology evidence is often embedded indirectly in outcome text or colonoscopy prose. The parser currently does not map those cases into a defensible biopsy-date field.

### 4. MMR extraction is too sparse

`Histology: MMR status(g/h)` is populated only twice.

This field works for clearly phrased cases such as `MMR deficient`, but the implementation is narrow and likely misses alternative phrasing or context placement. If MMR is clinically important for the intended downstream use, this needs more systematic coverage.

### 5. CT and MRI extraction is partial, not comprehensive

The Codex parser does extract some CT and MRI values, but coverage remains modest:
- `Baseline CT: Date(h)` -> 19 rows
- `Baseline CT: T(h)` -> 20 rows
- `Baseline CT: N(h)` -> 19 rows
- `Baseline CT: M(h)` -> 27 rows
- `Baseline MRI: date(h)` -> 12 rows
- `Baseline MRI: mrT(h)` -> 14 rows
- `Baseline MRI: mrN(h)` -> 12 rows

This is useful progress, but still incomplete. The source text contains more imaging detail than the current counts suggest. The present parser is not yet robust to:
- modality wording variation
- different punctuation around dates
- multi-sentence imaging descriptions
- cases where staging is implied in a nearby sentence rather than in the same segment

### 6. Previous-cancer extraction may over-normalize

`Demographics: Previous cancer...` is populated for all 50 rows, mostly as `No`.

That gives good completeness, but it also introduces a risk: the code currently defaults to `No` whenever it does not detect a prior-cancer phrase. That may be acceptable for this synthetic dataset, but it is a stronger assumption than leaving the field blank.

This is a tradeoff decision, not an outright bug. It should be reviewed before treating the field as reliable.

### 7. Treatment-approach mapping is heuristic and coarse

`1st MDT: Treatment approach ...` is populated in 27 rows using broad keyword mapping:
- `FOXTROT` -> chemotherapy
- `CRT` -> nCRT
- `watch and wait` -> Papillon +/- EBRT
- surgery-related terms -> straight to surgery

This is helpful as a first pass, but it is still heuristic compression of free text. The mapping should not yet be treated as clinically final.

### 8. The MDT decision field is over-broad

`MDT (after 6 week: Decision)` is populated in all 50 rows using the full outcome row text.

That guarantees coverage, but it is not a semantically clean decision field. In many rows it still contains mixed content:
- imaging summaries
- histology mentions
- recommendations
- actual decisions

This is useful for retaining signal, but not yet fully normalized.

## Code-Level Causes

The main reasons for the gaps are visible in the current extractor design:

- endoscopy extraction only supports two narrow regex patterns and does not reliably split type, date, and findings across wider phrasing patterns
- histology date extraction only searches for explicit biopsy-date wording
- CT/MRI extraction only uses the first matching segment for each modality rather than combining evidence across sections
- treatment-approach classification is keyword-driven and intentionally shallow
- the pipeline writes aligned columns after extraction, but reindexing only guarantees schema shape, not field completeness

These are all fixable, but they should be treated as parser-scope gaps, not styling gaps.

## What Is Already Good Enough

These areas are in a usable first-pass state:
- workbook styling and familiarity
- sheet naming and presentation
- demographics extraction for MRN, NHS number, initials, DOB, and gender in most rows
- diagnosis extraction in all rows
- first-pass CT/MRI staging extraction in a meaningful subset of rows
- clean separation between the Codex extractor and the earlier Gemini implementation

The main remaining work is on extraction breadth and normalization depth.

## Recommended Next Focus

If continuing the Codex implementation, the next priorities should be:

1. Fix `Endoscopy: date(f)` and `Histology: Biopsy date(g)`.
2. Improve CT and MRI extraction by handling multiple modality mentions per case.
3. Decide whether `Previous cancer = No` should remain a default or become blank when not evidenced.
4. Normalize the MDT decision field so it separates summary text from actionable decision text.
5. Add targeted tests for real cases that exercise flexi-sig, MRI-heavy, and prior-cancer scenarios.

## Conclusion

The Codex implementation is already a better baseline than the earlier Gemini extractor, but it is still a partial schema implementation.

The biggest remaining gaps are:
- missing endoscopy dates
- missing histology biopsy dates
- limited follow-up-field coverage
- partial imaging extraction
- over-broad use of free text in the MDT decision field

That is a workable state for a first alternative implementation, but not yet a complete solution.

## Signature

Prepared by Codex.
