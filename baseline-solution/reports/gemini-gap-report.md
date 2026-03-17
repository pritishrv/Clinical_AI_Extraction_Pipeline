# Gemini Gap Report

**Date:** March 15, 2026

**Prepared by:** Codex

## Scope

This report compares:
- generated workbook: `baseline-solution/output/generated-database-gemini.xlsx`
- reference workbook: `data/hackathon-database-prototype.xlsx`

The root [`README.md`](../../README.md) states that `data/hackathon-database-prototype.xlsx` serves as the "ground truth" or expected output.

## Summary

Gemini's solution produces a workbook with the correct 88-column schema and 50 generated rows, but extraction coverage is still very limited.

The main issue is not missing columns. The main issue is under-population of clinically relevant fields.

The reference workbook also has an important limitation: it contains only one populated data row on sheet `Prototype V1`. That means it behaves more like a schema/example workbook than a full 50-case gold dataset, so direct row-by-row accuracy comparison is only partially possible.

## Workbook Structure

Reference workbook:
- path: `data/hackathon-database-prototype.xlsx`
- sheets: `Prototype V1`
- shape: 1 row x 88 columns

Generated workbook:
- path: `baseline-solution/output/generated-database-gemini.xlsx`
- sheets: `Sheet1`
- shape: 50 rows x 88 columns

Structural observations:
- column count matches
- column ordering matches
- sheet name does not match
- generated row count is much higher than the reference workbook because the reference workbook only contains one populated example row

## Coverage Findings

Top populated columns in the generated workbook:
- `Histology: Biopsy result(g)` -> 50 populated rows
- `1st MDT: date(i)` -> 50 populated rows
- `Endoscopy: Findings(f)` -> 8 populated rows
- `Demographics: DOB(a)` -> 2 populated rows
- `Demographics: Gender(e)` -> 2 populated rows
- `Demographics: MRN(c)` -> 2 populated rows
- `Demographics: Initials(b)` -> 2 populated rows
- `Demographics: NHS number(d)` -> 2 populated rows
- `Baseline CT: T(h)` -> 2 populated rows
- `Baseline CT: N(h)` -> 2 populated rows
- `Baseline CT: M(h)` -> 2 populated rows
- `MDT (after 6 week: Decision)` -> 2 populated rows
- `Histology: MMR status(g/h)` -> 1 populated row

Coverage concerns:
- 75 of 88 columns are completely empty in the generated workbook
- several fields that are populated even in the single prototype row are blank in Gemini's output
- the generated workbook is therefore workbook-shaped, but not yet high-coverage

## Best Match Against The Prototype Row

Because the reference workbook contains only one populated data row, the most useful direct comparison is to find the best matching generated row against that single prototype row.

Best matching generated row:
- generated row index: 48
- normalized field matches: 8 of 12 populated prototype fields

Matched fields:
- `Demographics: DOB(a)`
- `Demographics: Initials(b)`
- `Demographics: MRN(c)`
- `Demographics: NHS number(d)`
- `Demographics: Gender(e)`
- `Endoscopy: Findings(f)`
- `Histology: Biopsy result(g)`
- `Histology: MMR status(g/h)`

Missing or mismatched fields:
- `Demographics: Previous cancer ...` -> generated blank, prototype `No`
- `Endoscopy: date(f)` -> generated blank, prototype `Missing`
- `Endosopy type ...` -> generated blank, prototype `Colonoscopy complete`
- `Histology: Biopsy date(g)` -> generated blank, prototype `Missing`

Interpretation:
- identity fields can sometimes be extracted
- one histology field and one endoscopy findings field can sometimes be extracted
- support for additional endoscopy and histology metadata is still incomplete
- the extractor does not currently preserve explicit "Missing" values from the source/prototype style

## Validator Gaps

The current validator in [`baseline-solution/src/validate_output.py`](../src/validate_output.py) is too weak to support reliable acceptance.

Observed limitations:
- it checks row counts only
- it checks whether the prototype columns exist
- it checks whether one prototype NHS number appears somewhere in the generated workbook
- it does not compare field population levels
- it does not compare row-level alignment
- it does not compare cell-level agreement
- it can report success even when extraction quality is still poor

This is visible in [`baseline-solution/src/validate_output.py`](../src/validate_output.py), especially around the column-presence check and the single-NHS-number check.

## Extractor Gaps

The extractor in [`baseline-solution/src/extract_fields.py`](../src/extract_fields.py) is currently narrow and heuristic-heavy.

Observed limitations:
- many target columns have no extraction logic at all
- `Histology: Biopsy result(g)` is populated from the `Diagnosis:` line, which is not a reliable general mapping
- endoscopy date, endoscopy type, biopsy date, and previous cancer status are not being extracted even where the prototype expects them
- most of the prototype schema is still unsupported

Practical effect:
- the pipeline in [`baseline-solution/src/pipeline.py`](../src/pipeline.py) aligns the generated DataFrame to the template columns, but that only guarantees the schema shape, not the data quality

## Most Important Gaps To Close Next

1. Improve validation so it measures:
- populated field coverage by column
- normalized row-level comparisons where possible
- exact and normalized match counts
- blank-versus-missing behavior

2. Extend extraction for fields already evidenced in the prototype row:
- previous cancer status
- endoscopy date
- endoscopy type
- histology biopsy date

3. Audit the source `.docx` structure more deeply so extraction logic is based on actual field patterns rather than optimistic regex assumptions.

4. Decide whether the prototype workbook is truly the full ground truth or only an example row plus schema.

## Conclusion

Gemini's implementation has produced a usable first-pass workbook and matched the expected column schema, but it has not yet reached acceptable extraction coverage.

The main gap is under-extraction, not schema mismatch.

The most immediate next step should be to strengthen validation and then extend extraction for the small set of fields that are already demonstrably present in the prototype row.

## Signature

Prepared by Codex.
