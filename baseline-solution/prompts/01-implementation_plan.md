# 01 Implementation Plan

Author: Codex

## Prompt Purpose

Use this prompt to instruct an implementation agent to build the first executable version of the standard solution for this repository.

## Prompt

You are implementing the baseline solution for the Clinical AI Hackathon repository.

Your goal is to build a conservative, auditable pipeline that transforms:
- `data/hackathon-mdt-outcome-proformas.docx`

into an Excel workbook aligned as closely as possible with:
- `data/hackathon-database-prototype.xlsx`

You must work inside the `baseline-solution/` area unless there is a strong reason not to.

### Context you must read first

Before writing code, read:
- `baseline-solution/README.md`
- `baseline-solution/work-diary.md`
- `docs/specification.md`
- `docs/minutes_february_12.md`
- `docs/minutes_march_2nd.md`

### Objective

Build a first-pass implementation that:
- ingests the `.docx` source document
- segments it into individual MDT cases
- extracts a minimal but useful set of clinical fields
- normalizes repeated patient discussions into longitudinal rows
- writes the result to an Excel workbook
- validates the generated workbook against the prototype workbook

### Output workbook naming

The generated workbook filename must include an agent suffix.

Use this pattern:
- `<base-name>-<agent>.xlsx`

Examples:
- Codex -> `generated-database-codex.xlsx`
- Gemini -> `generated-database-gemini.xlsx`

Write the workbook into:
- `baseline-solution/output/`

### Engineering constraints

You must follow these rules:
- prefer deterministic parsing over opaque end-to-end generation
- do not invent clinical facts that are not supported by the source text
- prefer blank cells over guessed values
- keep extraction logic inspectable and testable
- separate raw parsing, field extraction, normalization, export, and validation
- preserve repeated patient discussions as sequential longitudinal events
- log or surface ambiguous cases instead of silently guessing

### First implementation scope

The first useful version only needs to extract:
- patient identifier
- discussion date or stable discussion order
- cancer type or diagnosis
- stage
- TNM
- question for discussion
- prior treatment
- imaging summary
- pathology summary
- MDT outcome

### Required work order

Work in this order:

1. Inspect `data/hackathon-mdt-outcome-proformas.docx` programmatically and document its structure.
2. Inspect `data/hackathon-database-prototype.xlsx` and identify sheets, columns, and row patterns.
3. Create a schema map from likely source evidence to target output columns.
4. Implement document loading and case segmentation.
5. Verify that the expected number of cases can be recovered.
6. Implement minimal field extraction for the first-pass field set.
7. Normalize extracted data into longitudinal rows.
8. Export the result to Excel.
9. Implement validation against the prototype workbook.
10. Document any unresolved ambiguities or mismatches.

Do not skip the inspection and schema-mapping stages.

### Recommended directory layout

Create or use files along these lines:

```text
baseline-solution/
├── README.md
├── work-diary.md
├── prompts/
│   └── 01-implementation_plan.md
├── src/
│   ├── load_docx.py
│   ├── segment_cases.py
│   ├── extract_fields.py
│   ├── normalize_rows.py
│   ├── write_excel.py
│   └── validate_output.py
├── tests/
│   ├── test_segmentation.py
│   ├── test_extraction.py
│   └── test_validation.py
└── output/
    └── generated-database-<agent>.xlsx
```

### Acceptance criteria

The first pass is acceptable when:
- it runs end to end on the supplied `.docx`
- it produces an Excel workbook without manual editing
- the workbook structure is materially aligned with the prototype
- missing data remains blank rather than guessed
- repeated patient events remain longitudinal
- discrepancies against the prototype are identified explicitly

### What to avoid

Do not:
- collapse everything into one large script
- redesign the entire repo structure without cause
- replace deterministic extraction with a vague "AI pipeline"
- infer undocumented transformations without evidence from the source or prototype
- optimize for production deployment before the baseline works

### Expected output of your implementation session

By the end of the session, you should ideally have:
- code under `baseline-solution/src/`
- at least basic tests for segmentation and extraction
- a generated workbook under `baseline-solution/output/` using the required agent suffix naming convention
- a short note on what matches the prototype and what still does not

## Author Attribution

This implementation prompt was authored by Codex.
