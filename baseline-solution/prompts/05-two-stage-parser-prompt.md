# 05 Two-Stage Parser Prompt

Author: Claude Code

## Prompt Purpose

This prompt specifies a redesigned extraction pipeline that replaces the current single-pass
regex extractor with a two-stage architecture:

1. **Stage 1** — `.docx` → `.json` (deterministic parser only)
2. **Stage 2** — `.json` → verified `.json` (grep-based provenance check)
3. **Stage 3** — verified `.json` → `.xlsx` (assembly only)

It captures design decisions made before implementation begins so that any agent continuing
this work starts from a shared, agreed position.

---

## Background and Motivation

The current Codex and Claude extractors parse the `.docx` and write the `.xlsx` in a single
pass. This creates two problems:

- **Extraction and assembly are entangled.** A bug in a regex silently produces a wrong cell
  value with no way to distinguish "extracted but wrong" from "not extracted".
- **There is no provenance.** For any cell in the generated workbook, there is no record of
  what source text it came from or whether that source text actually existed in the document.

The two-stage architecture solves both problems by introducing an intermediate `.json`
representation that carries source evidence alongside each extracted value, and a verification
step that checks that evidence against the original document before the value is written to
the workbook.

---

## Design Decisions (Agreed Before Implementation)

### Decision 1: Stage 1 is a deterministic parser only — no LLM calls

The source document contains real or realistic patient data. In a real NHS deployment, sending
patient data to a cloud API (OpenAI, Anthropic, Google, etc.) would violate data governance
and information governance requirements. Stage 1 must therefore use only deterministic,
locally-executed parsing: regex, rule-based heuristics, and structural document parsing.

No LLM extraction at Stage 1. Ever.

This constraint also has a benefit: deterministic parsers are reproducible. The same input
always produces the same output, which makes regression testing straightforward.

### Decision 2: No colour-coding in the output workbook

Adding cell colours to flag verification status would change the visual presentation of the
workbook and could confuse clinicians reviewing the output. Instead, a dedicated verification
flag column is added at the far right of the workbook (after all clinical columns) to carry
the human-review signal without altering the clinical data presentation.

### Decision 3: Incomplete or low-confidence fields are flagged for human verification

Fields where the parser could not extract a value, or extracted a value with low confidence,
should not be silently left blank without explanation. Instead, the verification flag column
records the reason so a human reviewer knows what to look for.

Typical cases that trigger a human-verification flag:
- Name not found or could not be parsed into initials
- Gender not found in demographics row
- Date field empty (endoscopy date, biopsy date, CT date)
- TNM stage partially extracted (e.g. T found but N and M missing)
- MDT decision text suspiciously short or empty

### Decision 4: Inferred fields are included in the output but flagged

Some fields cannot be verified by a direct text match because they are derived from other
fields. Examples:
- Initials derived from a parsed name
- Biopsy date inferred from a dated colonoscopy where findings mention cancer or biopsy

These fields should still appear in the output workbook — they are clinically useful — but
the verification flag column must record that the value is inferred rather than directly
extracted, so a human reviewer can confirm or correct it.

---

## Architecture

```
baseline-solution/
├── src/
│   ├── stage1_extract_to_json.py    # .docx → per-case .json files
│   ├── stage2_verify_json.py        # per-case .json → verified .json files
│   ├── stage3_assemble_excel.py     # verified .json files → .xlsx
│   └── pipeline_two_stage.py        # orchestrates all three stages end to end
├── output/
│   ├── json/
│   │   ├── case_000_raw.json        # raw extraction output per case
│   │   └── case_000_verified.json   # post-verification output per case
│   └── generated-database-claude-v2.xlsx
└── tests/
    ├── test_stage1_extraction.py
    ├── test_stage2_verification.py
    └── test_stage3_assembly.py
```

---

## Stage 1: .docx → .json

### One JSON file per case

Each of the 50 cases produces one `case_NNN_raw.json` file. This keeps failures isolated:
a bad parse on case 12 does not affect case 13.

### JSON schema

Each field in the JSON carries:
- `value` — the extracted value (string, or empty string if not found)
- `source_text` — the raw text from the document that the value was extracted from
- `source_row` — the table row index (0–7) the source text came from
- `method` — one of: `"regex"`, `"heuristic"`, `"inferred"`, `"default"`
- `verified` — boolean, set to `false` at extraction time, updated by Stage 2

Example schema for one case:

```json
{
  "case_index": 0,
  "demographics": {
    "nhs_number": {
      "value": "9990000001",
      "source_text": "NHS Number: 9990000001",
      "source_row": 1,
      "method": "regex",
      "verified": false
    },
    "dob": {
      "value": "26/05/1970",
      "source_text": "DOB: 26/05/1970  Age: 56 Years",
      "source_row": 1,
      "method": "regex",
      "verified": false
    },
    "initials": {
      "value": "AO",
      "source_text": "Name: Alice O'Brien",
      "source_row": 1,
      "method": "inferred",
      "verified": false
    },
    "gender": {
      "value": "",
      "source_text": "",
      "source_row": 1,
      "method": "regex",
      "verified": false
    }
  },
  "endoscopy": {
    "date": {
      "value": "20/10/2024",
      "source_text": "Flexi sig 20/10/2024: rectal cancer, 2.5cm across",
      "source_row": 5,
      "method": "regex",
      "verified": false
    },
    "type": {
      "value": "flexi sig",
      "source_text": "Flexi sig 20/10/2024: rectal cancer, 2.5cm across",
      "source_row": 5,
      "method": "regex",
      "verified": false
    },
    "findings": {
      "value": "rectal cancer, 2.5cm across, fixed, abnormal PIT pattern, unsuitable for local excision",
      "source_text": "Flexi sig 20/10/2024: rectal cancer, 2.5cm across, fixed, abnormal PIT pattern, unsuitable for local excision",
      "source_row": 5,
      "method": "regex",
      "verified": false
    }
  },
  "histology": {
    "biopsy_result": {
      "value": "Sigmoid adenocarcinoma",
      "source_text": "Diagnosis: Sigmoid adenocarcinoma",
      "source_row": 3,
      "method": "regex",
      "verified": false
    },
    "biopsy_date": {
      "value": "20/10/2024",
      "source_text": "Flexi sig 20/10/2024: rectal cancer",
      "source_row": 5,
      "method": "inferred",
      "verified": false
    },
    "mmr_status": {
      "value": "",
      "source_text": "",
      "source_row": -1,
      "method": "regex",
      "verified": false
    }
  },
  "staging": {
    "ct": {
      "date": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "t": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "n": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "m": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "emvi": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false }
    },
    "mri": {
      "date": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "mrt": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "mrn": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "mremvi": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "mrcrm": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false },
      "mrpsw": { "value": "", "source_text": "", "source_row": -1, "method": "regex", "verified": false }
    }
  },
  "mdt": {
    "date": { "value": "07/03/2025", "source_text": "Colorectal Multidisciplinary Meeting 07/03/2025(i)", "source_row": -1, "method": "regex", "verified": false },
    "treatment_approach": { "value": "downstaging nCRT", "source_text": "CRT", "source_row": 7, "method": "heuristic", "verified": false },
    "decision": { "value": "CRT | CT adrenal study | Completion colonoscopy and tattoo", "source_text": "CRT | CT adrenal study | Completion colonoscopy and tattoo", "source_row": 7, "method": "regex", "verified": false }
  }
}
```

### Method values and their meaning

| Method | Meaning |
|--------|---------|
| `regex` | Value extracted by a regular expression directly from source text |
| `heuristic` | Value derived by a keyword-mapping rule (e.g. "CRT" → "downstaging nCRT") |
| `inferred` | Value derived from another field's evidence (e.g. biopsy date from colonoscopy date) |
| `default` | Value assigned as a default when no evidence was found (e.g. `Previous cancer = No`) |

---

## Stage 2: Verification

Stage 2 reads each `case_NNN_raw.json`, verifies each field, and writes
`case_NNN_verified.json` with updated `verified` flags.

### Verification rules by method

**regex fields:**
1. Check that `source_text` is a substring of the raw case text extracted from the `.docx`
   for that case (case-insensitive).
2. Check that `value` (after date normalisation) is a substring of `source_text`
   (case-insensitive).
3. If both checks pass: `verified = true`.
4. If either check fails: `verified = false`, add `"verification_failure"` key explaining
   which check failed.

**heuristic fields:**
1. Check that `source_text` is a substring of the raw case text (same as regex check 1).
2. The normalized value does not need to appear verbatim in `source_text` (it is a mapping).
3. If check 1 passes: `verified = true`.
4. Mark with `"method": "heuristic"` so the assembly stage can flag it for human review.

**inferred fields:**
1. Check that `source_text` (the evidence the inference was drawn from) is a substring of
   the raw case text.
2. The inferred value itself is not checked against the source (it cannot be — it was derived).
3. If check 1 passes: `verified = true` with `"method": "inferred"` preserved.
4. Always flagged for human verification regardless of verified status.

**default fields:**
1. Always `verified = false`.
2. Always flagged for human verification.
3. The value is still written to the Excel output, but the flag column records
   `"default — no source evidence"`.

### Date normalisation for verification

Before checking whether a date value appears in its source text, normalise both to a
canonical form (e.g. strip leading zeros, try both `/` and `-` separators). Do not fail
verification on a date solely because the separator differs.

---

## Stage 3: Assembly (.json → .xlsx)

### Field mapping

A separate mapping file (or dict) translates the JSON hierarchy to prototype column names:

```python
FIELD_MAP = {
    "demographics.nhs_number": "Demographics: \nNHS number(d)",
    "demographics.dob": "Demographics: \nDOB(a)",
    "demographics.initials": "Demographics: Initials(b)",
    "demographics.gender": "Demographics: \nGender(e)",
    "endoscopy.date": "Endoscopy: date(f)",
    "endoscopy.type": "Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) ",
    "endoscopy.findings": "Endoscopy: Findings(f)",
    "histology.biopsy_result": "Histology: Biopsy result(g)",
    "histology.biopsy_date": "Histology: Biopsy date(g)",
    "histology.mmr_status": "Histology: \nMMR status(g/h)",
    "staging.ct.date": "Baseline CT: Date(h)",
    "staging.ct.t": "Baseline CT: T(h)",
    "staging.ct.n": "Baseline CT: N(h)",
    "staging.ct.m": "Baseline CT: M(h)",
    "staging.ct.emvi": "Baseline CT: EMVI(h)",
    "staging.mri.date": "Baseline MRI: date(h)",
    "staging.mri.mrt": "Baseline MRI: mrT(h)",
    "staging.mri.mrn": "Baseline MRI: mrN(h)",
    "staging.mri.mremvi": "Baseline MRI: mrEMVI(h)",
    "staging.mri.mrcrm": "Baseline MRI: mrCRM(h)",
    "staging.mri.mrpsw": "Baseline MRI: mrPSW(h)",
    "mdt.date": "1st MDT: date(i)",
    "mdt.treatment_approach": "1st MDT: Treatment approach \n(TNT, downstaging chemotherapy, downstaging nCRT, downstaging shortcourse RT, Papillon +/- EBRT, straight to surgery(h)",
    "mdt.decision": "MDT (after 6 week: Decision ",
}
```

### Verification flag column

A column named `Human Verification Required` is appended after all clinical columns.

Its value for each row is a pipe-separated list of field names that need review. Empty if
the row passed all verification checks.

Examples:
- `""` — all fields verified
- `"gender | endoscopy.date"` — gender not found, endoscopy date not found
- `"initials (inferred) | histology.biopsy_date (inferred)"` — inferred values present
- `"demographics.previous_cancer (default)"` — default value used, no source evidence

### Rules for what appears in the flag column

| Condition | Flag text |
|-----------|-----------|
| `verified = false` and `method = "regex"` | `<field_name>` |
| `method = "heuristic"` | `<field_name> (heuristic)` |
| `method = "inferred"` | `<field_name> (inferred)` |
| `method = "default"` | `<field_name> (default — no source evidence)` |
| `value = ""` for a clinically important field | `<field_name> (missing)` |

Clinically important fields that must always be flagged if empty:
- `demographics.initials`
- `demographics.gender`
- `demographics.nhs_number`
- `demographics.dob`
- `histology.biopsy_result`
- `mdt.decision`

---

## Tests Required

### test_stage1_extraction.py
- Verify 50 JSON files are produced
- Verify required top-level keys exist in each file
- Verify `source_text` is never `None` (empty string is acceptable)
- Verify `method` is always one of the four allowed values
- Spot-check specific known values for cases with clear patterns (e.g. case 40 flexi sig date)

### test_stage2_verification.py
- Given a synthetic JSON with a known good `source_text` and matching `value`, verify it
  passes
- Given a synthetic JSON with a `source_text` that does not appear in the case text, verify
  it fails
- Given a synthetic JSON with `method = "inferred"`, verify it is flagged for human
  review regardless of other checks
- Given a synthetic JSON with `method = "default"`, verify `verified = false` always

### test_stage3_assembly.py
- Verify the output workbook has 50 rows
- Verify the `Human Verification Required` column is present
- Verify that a row with no failures has an empty flag cell
- Verify that a row with an inferred field has the field name in the flag cell
- Verify workbook styling matches the prototype (regression guard)

---

## Output Naming

The output workbook for this pipeline should be named:

```
output/generated-database-claude-v2.xlsx
```

The `v2` suffix distinguishes this from the single-pass Claude extractor output.

---

## Implementation Order

Work in this order:

1. Define the JSON schema as a Python dataclass or TypedDict for type safety.
2. Implement `stage1_extract_to_json.py` — port the existing Claude extractor logic but
   write JSON instead of a DataFrame. Add `source_text` capture to every extraction call.
3. Write `tests/test_stage1_extraction.py` and verify it passes.
4. Implement `stage2_verify_json.py` — read raw JSON, run verification rules, write
   verified JSON.
5. Write `tests/test_stage2_verification.py` and verify it passes.
6. Implement `stage3_assemble_excel.py` — read verified JSON, apply field map, append flag
   column, write styled workbook.
7. Write `tests/test_stage3_assembly.py` and verify it passes.
8. Implement `pipeline_two_stage.py` to orchestrate all three stages.
9. Run the full pipeline, compare coverage against the single-pass Claude output.
10. Update `work-diary.md`.

Do not skip the JSON schema definition step. Agreeing the schema before writing the extractor
prevents the verification step from needing to reverse-engineer what the extractor meant to
produce.

---

## Working Rules

All rules from `prompts/02-claude-code-handoff.md` remain in force. Additional rules for
this prompt:

- Stage 1 must never make a network call or invoke an LLM. Local execution only.
- The `Human Verification Required` column must be the last column in the workbook.
- Do not change cell colours or formatting in the clinical data columns.
- Inferred and default values must appear in the output (they are useful) but must always
  be flagged.
- Prefer blank `value` to a guessed value. If a field cannot be extracted with defensible
  evidence, leave `value` as `""` and flag it.
- The JSON files in `output/json/` should be committed alongside the workbook so the
  extraction evidence is preserved in the repository.

---

## Author Attribution

This prompt was authored by Claude Code.
