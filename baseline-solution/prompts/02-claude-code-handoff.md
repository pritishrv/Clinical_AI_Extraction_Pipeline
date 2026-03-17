# 02 Claude Code Handoff

Author: Codex

## Prompt Purpose

Use this prompt to hand the current `baseline-solution/` state to Claude Code with the necessary context, constraints, and priorities already established.

## Prompt

You are continuing work in `baseline-solution/` for the Clinical AI Hackathon repository.

Before making changes, read:
- `baseline-solution/README.md`
- `baseline-solution/work-diary.md`
- `baseline-solution/reports/gemini-gap-report.md`
- `baseline-solution/reports/codex-gap-report.md`
- `baseline-solution/prompts/00-prompt-starter.md`
- `baseline-solution/prompts/01-implementation_plan.md`

## What Already Exists

There are two implementation attempts in this directory.

### 1. Gemini attempt

Relevant files:
- `baseline-solution/src/extract_fields.py`
- `baseline-solution/src/pipeline.py`
- `baseline-solution/output/generated-database-gemini.xlsx`
- `baseline-solution/reports/gemini-gap-report.md`

What it achieved:
- segmented the source `.docx`
- produced an initial workbook aligned to the prototype columns

Main weaknesses:
- very low extraction coverage
- weak validator
- many clinically important columns left empty

### 2. Codex attempt

Relevant files:
- `baseline-solution/src/codex_extract_fields.py`
- `baseline-solution/src/pipeline_codex.py`
- `baseline-solution/src/write_excel.py`
- `baseline-solution/output/generated-database-codex.xlsx`
- `baseline-solution/reports/codex-gap-report.md`

What it improved:
- materially better extraction coverage
- separate extractor path for cleaner comparison
- workbook styling copied from the clinician-prepared prototype
- agent-suffixed workbook naming

Known measured improvement:
- Gemini non-empty cells: `127`
- Codex non-empty cells: `661`
- Gemini best normalized match to the populated prototype row: `8/12`
- Codex best normalized match to the populated prototype row: `10/12`

## Critical Context

The file `data/hackathon-database-prototype.xlsx` is described in the root README as the "ground truth" or expected output, but in practice it contains only one populated data row.

Treat it as:
- the canonical schema
- the canonical presentation template
- a useful example row

Do not assume it is a complete 50-row gold dataset.

## Current Codex Gaps

The most important remaining gaps are:
- `Endoscopy: date(f)` is still empty
- `Histology: Biopsy date(g)` is still empty
- 61 target columns remain empty
- follow-up pathway fields are mostly unimplemented
- treatment-course fields are mostly unimplemented
- MDT decision text is still too broad and not fully normalized
- some defaults are heuristic and should be reviewed before being treated as reliable clinical outputs

Do not spend time re-solving already solved workbook styling unless you discover a regression.

## Working Rules

- Work inside `baseline-solution/` unless there is a strong reason not to.
- Preserve both the Gemini and Codex implementations for comparison unless the user explicitly asks to remove one.
- Do not overwrite the Codex workbook with a non-agent-suffixed filename.
- Use the required output naming convention:
  - `generated-database-<agent>.xlsx`
- Keep the prototype workbook styling in the exported result.
- Prefer deterministic parsing and explicit heuristics over vague end-to-end AI extraction.
- Do not invent clinical facts.
- Prefer blank cells to guesses.
- If you improve extraction, add or update focused tests.

## Recommended Direction

If you continue implementation, continue from the Codex path rather than the Gemini path unless you find a concrete reason to switch.

Best next targets:
1. Improve `Endoscopy: date(f)`.
2. Improve `Histology: Biopsy date(g)`.
3. Tighten CT and MRI extraction around multi-segment cases.
4. Normalize the MDT decision field into cleaner actionable text.
5. Add targeted tests for real cases that exercise the improved logic.

## Validation Expectations

Do not rely only on:
- row counts
- column presence
- a single NHS-number check

At minimum, validate:
- populated-column coverage
- normalized comparison against the populated prototype row
- no regression in workbook presentation
- whether your changes improve the Codex workbook compared with the previous state

## Required Diary Update

When you finish any work, update:
- `baseline-solution/work-diary.md`

Your entry should state:
- what you inspected
- what you changed
- why
- if applicable, what prompt you followed

Each entry or grouped entry block must be signed by the agent.

## Output Expectation

If you produce a new workbook, it should remain in:
- `baseline-solution/output/`

and should use your agent suffix.

Example:
- `generated-database-claude.xlsx`

## Author Attribution

This Claude Code handoff prompt was authored by Codex.
