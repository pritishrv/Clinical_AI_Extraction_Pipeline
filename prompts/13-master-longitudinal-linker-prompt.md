# 13 The Master Longitudinal Linker Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies the **v4 Master Longitudinal Linker**. It is the final "Production Grade" implementation designed to maximize density while maintaining perfect chronological order. 

It abandons coordinate-based extraction and uses **Timeline-Aware Slotting** to fill the 88-column schema.

---

## Background and Motivation

- **v1 Diamond** (1,102 cells) was high density but chronologically messy.
- **v2 Obsidian** (551 cells) was clean but too strict (it filtered out too much data).
- **v3 Grid** (236 cells) was too brittle (merged cells broke the coordinates).

**The v4 Master Solution:**
1.  **Exhaustive Harvester:** Capture every piece of text from the document.
2.  **Fact Chronology:** Group facts by Patient ID and sort them by the document date.
3.  **Dynamic Slotting:** Instead of hard-coding "This is Baseline," the system uses a **Sequential Buffer**:
    - 1st T-Stage found -> `Baseline MRI`
    - 2nd T-Stage found -> `2nd MRI`
    - 3rd T-Stage found -> `12 week MRI`
    - This ensures **zero data loss** while maintaining journey logic.

---

## Technical Stack

- **Miner:** Regex-based Exhaustive Harvester (Table + Paragraph).
- **Linker:** Pandas GroupBy + Chronological Sort logic.
- **Assembler:** openpyxl with "Recursive Slotting" and Evidence Comments.

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage1_master_harvester.py    # Pulls everything into a flat Fact List
│   ├── stage2_timeline_slotter.py    # Groups by Patient & Slots data chronologically
│   └── pipeline_v10_master.py        # v4 Orchestrator
└── output/
    └── generated-database-v10-master.xlsx
```

---

## Validation Strategy

- **Density Target:** > 1,500 non-empty cells.
- **Recall:** Capture 100% of staging data across the patient journey.
- **Auditability:** Comments anchored to the exact document index and date.

---

## Author Attribution

This prompt was authored by Gemini CLI.
