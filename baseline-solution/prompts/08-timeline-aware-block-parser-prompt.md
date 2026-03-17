# 08 Timeline-Aware Block Parser Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies a **Platinum Standard** extraction pipeline designed to break the 675-cell density barrier. It moves away from global text parsing and implements a **Chronological Zonal Architecture**. 

The pipeline treats each clinical proforma as a sequence of **Timeline Blocks**, ensuring that entities (like T-Stage or Dates) are correctly assigned to their specific clinical event (Baseline vs. 2nd MRI vs. 12-week Follow-up).

---

## Background and Motivation

Previous iterations (Regex, Global NER) plateaued at ~530 cells because they struggled with **Context Ambiguity**. A proforma may mention "T3" three different times in different contexts. Without "knowing" where it is in the patient journey, the agent cannot safely populate the 88-column schema.

**The Timeline-Aware Solution:**
1.  **Segmentation:** Divide the proforma into four distinct zones: `REFERRAL`, `BASELINE`, `PRIMARY_TREATMENT`, and `FOLLOW_UP`.
2.  **Zonal Anchoring:** Restrict the search for specific Excel columns to their corresponding zones.
3.  **Fuzzy Key-Value Mapping:** Capture "trapped" data by identifying `Key: Value` pairs and using semantic similarity to map them to the 88 target headers.

---

## Industry Standard Tech Stack

- **Segmenter:** `python-docx` + Regex-based Header Detection.
- **Semantic Mapper:** `Sentence-Transformers` (local) for fuzzy key-to-column mapping.
- **Clinical Brain:** `MedSPaCy` for zonal entity extraction and negation detection.
- **Assembly Engine:** `openpyxl` with forced string-formatting for clinical safety.

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage1_zonal_segmentation.py   # .docx -> Zonal JSON (Referral, Baseline, etc.)
│   ├── stage2_fuzzy_kv_extraction.py  # Zonal JSON -> Key-Value Pairs -> 88-column Map
│   ├── stage3_clinical_inference.py   # Heuristic logic (e.g., FOLFOX -> Curative Goal)
│   └── pipeline_v5_platinum.py        # Orchestration
├── output/
│   ├── json_zonal/                    # Segmented context blocks
│   └── generated-database-platinum.xlsx
```

---

## Implementation Details

### Stage 1: Zonal Segmentation
Divide the proforma text using structural anchors:
- **Zone 1: Referral:** Patient Details to "Diagnosis".
- **Zone 2: Baseline:** "Staging" to "MDT Outcome".
- **Zone 3: Treatment:** Outcomes containing "Chemo", "Radiotherapy", or "Surgery".
- **Zone 4: Follow-up:** Any "Rediscuss", "2nd MRI", or "12-week" mentions.

### Stage 2: Fuzzy Key-Value Extraction
1.  Extract every line containing a colon (`:`).
2.  Compare the "Key" (left of colon) against the 88 Excel headers using Levenshtein distance or Embedding similarity.
3.  Assign the "Value" (right of colon) if the similarity score > 0.85.

### Stage 3: Clinical Inference (The "Wow Factor")
Implement a "Clinician Heuristic" layer:
- **Protocol Inference:** If "CAPOX" or "FOLFOX" is detected, auto-populate `Chemotherapy: Drugs`.
- **Intent Inference:** If "Watch and Wait" is detected, auto-populate `Watch and wait: Entered` as "Yes".
- **Staging Cleanup:** If `mrT3` is found in the `FOLLOW_UP` zone, map it to `2nd MRI: mrT`.

---

## Per-Stage Validation Strategy

### Stage 1: Segmentation Integrity
- **Metric:** Block Boundary Accuracy.
- **Goal:** 100% of "MDT Outcome" sections must be assigned to either Zone 2 or Zone 4 based on keywords.

### Stage 2: Mapping Precision
- **Metric:** Key-to-Column Match Rate.
- **Goal:** Zero "Cross-Contamination" (e.g., Baseline data appearing in Follow-up columns).

### Stage 3: End-to-End Density
- **Density Check:** Target **> 750 non-empty cells** across 50 cases.
- **Safety Check:** 100% verification that NHS numbers are formatted as clean integers.

---

## Engineering Constraints

1.  **Data Sovereignty:** All embedding models and similarity checks must run locally (e.g., `Sentence-Transformers`).
2.  **Auditability:** The intermediate Zonal JSON must preserve the `source_line_number` for every extracted field.
3.  **Graceful Degradation:** If a zone cannot be identified, fall back to the v4 Global NER logic.

---

## Implementation Order

1.  **Zonal Parser:** Build the structural segmenter for the 4 patient journey phases.
2.  **Fuzzy Engine:** Implement the semantic mapper for Key-Value pairs.
3.  **Inference Rules:** Code the oncology-specific logic for protocol-based filling.
4.  **Platinum Assembly:** Merge all streams into the final styled Excel.

---

## Author Attribution

This prompt was authored by Gemini CLI.
