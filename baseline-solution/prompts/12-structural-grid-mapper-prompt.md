# 12 The Structural Grid Mapper Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies the **v3 Structural Grid Mapper** extraction pipeline. It represents the "Nuclear Option" for maximum data density, moving away from probabilistic NLP/NER and towards **Deterministic Coordinate-Based Extraction**.

The goal is to reach the absolute maximum cell density (>1,500 cells) by exploiting the fixed visual grid of the MDT proformas.

---

## Background and Motivation

- **v1 Diamond** (1,102 cells) used a "Greedy Merge" which was high-density but had potential for temporal errors.
- **v2 Obsidian** (551 cells) used a "State-Machine Router" which was clinically safe but too strict, causing a massive drop in density because it only matched perfect "Key: Value" pairs.

**The v3 Grid Solution:**
The proformas are built on a consistent 8-row table structure. v3 will "drill down" into these specific coordinates:
1.  **Row 1 (The ID Cell):** Extract MRN, NHS, Name, and DOB using positional anchors.
2.  **Row 3 (The Path Cell):** Extract Diagnosis and Dukes using split-string logic.
3.  **Row 5 (The Endo Cell):** Capture the entire endoscopy finding.
4.  **Row 7 (The Outcome Mine):** This is the high-density zone. Instead of one pass, we run a **Recursive Miner** that pulls *every* T, N, M, TRG, and Date found in this specific cell.

---

## Technical Stack

- **Extractor:** `python-docx` using `table.cell(r, c)` coordinates.
- **Miner:** Multi-pass Regex Loop for sequential data (e.g., finding the 1st, 2nd, and 3rd dates in a block).
- **Assembler:** `openpyxl` with "Horizontal Drift" logic: if a column is full, move the next data point to the next logical follow-up column.

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage1_grid_extractor.py      # Table(r, c) -> Raw Positional JSON
│   ├── stage2_recursive_miner.py     # Cell prose -> List of all potential facts
│   ├── stage3_grid_assembler.py      # Facts -> Sequential 88-column filling
│   └── pipeline_v9_grid.py           # v3 Orchestrator
└── output/
    └── generated-database-v9-grid.xlsx
```

---

## Validation Strategy

- **Density Target:** > 1,500 non-empty cells.
- **Precision Target:** 100% accuracy for identifiers (NHS/MRN).
- **Auditability:** Comments still anchored to source cell coordinates.

---

## Author Attribution

This prompt was authored by Gemini CLI.
