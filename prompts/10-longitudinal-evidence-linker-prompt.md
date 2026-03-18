# 10 Longitudinal Evidence Linker Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies the **Diamond Standard (v7)** extraction pipeline. It moves beyond document-level parsing to **Patient-Level Longitudinal Tracking**. 

The goal is to link multiple proformas belonging to the same patient to create a single, comprehensive longitudinal record, while maintaining a perfect audit trail via "Evidence Anchoring."

---

## Background and Motivation

A single MDT proforma often only covers one phase of treatment. To fill all 88 columns (Baseline -> Treatment -> Follow-up -> Watch & Wait), the system must connect the dots between separate documents.

**The Longitudinal Solution:**
1.  **Patient Grouping:** Use NHS Numbers and MRNs to group the 50 cases into unique patient identities.
2.  **Timeline Assembly:** Order a patient's documents by MDT Date.
3.  **Cross-Document Filling:** Use data from later documents to fill the "empty" follow-up columns in the patient's master database entry.
4.  **Evidence Anchoring:** Every extracted value must be accompanied by its "Source Snippet" (the surrounding 15 words) to be stored as an Excel Comment.

---

## Technical Stack

- **Linker:** Python `pandas` GroupBy logic with fuzzy matching for names.
- **Evidence Miner:** Recursive Context Window extractor added to the Harvester.
- **Assembly:** `openpyxl` with **Comment Injection** for auditability.

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage1_exhaustive_harvester_v2.py # Now captures "Context Snippets"
│   ├── stage4_longitudinal_linker.py     # Connects cases by NHS Number
│   └── stage5_evidence_assembler.py      # Injects data + snippets into Excel
└── output/
    └── generated-database-v7-diamond.xlsx
```

---

## Implementation Details

### Stage 1: Evidence Harvesting
Modify the harvester to not just find `Key: Value`, but to capture the `Context` (the sentence containing the value).

### Stage 2: Patient Linking
1.  Identify unique patients using NHS Number.
2.  If NHS Number is missing, use MRN or a fuzzy match on Initials + DOB.
3.  Consolidate all extracted data for that identity into a single "Master Row."

### Stage 3: Comment Injection
When writing the Excel file, for every non-empty cell, create an **Excel Comment** containing:
`"Source: [Evidence Snippet] | Doc: Case_XXX"`

---

## Validation Strategy

- **Density Check:** Target **> 850 non-empty cells** (achieved by merging follow-up data into master records).
- **Audit Check:** Verify that clicking a cell in Excel reveals the source prose in a comment.
- **Safety Check:** Ensure that if two documents provide conflicting data (e.g., different T-stages), the system flags the conflict.

---

## Author Attribution

This prompt was authored by Gemini CLI.
