# 11 The Obsidian Standard (State-Machine Linker) Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies the **Obsidian Standard (v2)** extraction pipeline. It evolves the longitudinal linker into a **Clinical State Machine** that understands the chronological progression of a cancer patient (Baseline -> Neoadjuvant -> Surgery -> Follow-up).

The goal is to break the 1,102-cell barrier and double the schema breadth by correctly mapping time-dependent data (like 2nd and 3rd MRIs) to their specific Excel slots.

---

## Background and Motivation

The v1 Diamond model used a "greedy merge" where later documents filled gaps but often overwrote baseline data. In oncology, we need both: the state *before* chemo and the state *after* chemo.

**The State Machine Solution:**
1.  **Document Phase Classification:** For every proforma, determine its clinical phase:
    - `PHASE_0: Baseline` (Initial staging)
    - `PHASE_1: Post-Neoadjuvant` (After chemo/radio, before surgery)
    - `PHASE_2: Post-Surgical` (Pathology and surgical outcome)
    - `PHASE_3: Surveillance` (12-week and long-term follow-up)
2.  **Phase-Aware Mapping:** Instead of generic columns, data is routed based on phase:
    - `T-Stage` in `PHASE_0` -> `Baseline CT: T(h)`
    - `T-Stage` in `PHASE_1` -> `2nd MRI: mrT`
    - `T-Stage` in `PHASE_3` -> `12 week MRI: mrT`
3.  **Conflict Resolution:** If two documents in the same phase conflict, store both and flag for clinician review.

---

## Technical Stack

- **Phase Classifier:** Regex + Keyword scoring (e.g., "post-chemo" -> PHASE_1).
- **State Engine:** Python dictionary-based state tracker per Patient ID.
- **Assembly:** Enhanced `openpyxl` logic with phase-based column routing.

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage4_phase_classifier.py      # Tag cases with PHASE_0 to PHASE_3
│   ├── stage5_state_machine_linker.py  # Map data to phase-specific columns
│   └── pipeline_v8_obsidian.py         # The v2 Orchestrator
└── output/
    └── generated-database-v8-obsidian.xlsx
```

---

## Implementation Details

### Stage 1: Phase Classification
Use the `MDT Outcome` and paragraph headers to score each document:
- If contains "Post-treatment" or "Restaging" -> `PHASE_1`.
- If contains "Resection" or "Pathology" -> `PHASE_2`.
- If contains "Baseline" or "Primary" -> `PHASE_0`.

### Stage 2: State-Machine Routing
When merging patient data, use a routing table:
| Field | Phase 0 Slot | Phase 1 Slot | Phase 3 Slot |
| :--- | :--- | :--- | :--- |
| T-Stage | Baseline CT: T | 2nd MRI: mrT | 12 week MRI: mrT |
| MDT Date | 1st MDT Date | MDT (after 6 week) | MDT (after 12 week) |

---

## Validation Strategy

- **Breadth Check:** Target **> 60 unique columns** populated (Double the v1 breadth).
- **Temporal Check:** Verify that `Baseline MRI` and `2nd MRI` dates are in chronological order.
- **Obsidian Density:** Target **> 1,500 non-empty cells** across 50 cases.

---

## Author Attribution

This prompt was authored by Gemini CLI.
