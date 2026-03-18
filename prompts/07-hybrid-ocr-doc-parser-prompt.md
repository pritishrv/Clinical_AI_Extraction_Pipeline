# 07 Hybrid OCR and Structural Parser Prompt (Exhaustive)

Author: Gemini CLI

## Prompt Purpose

This prompt specifies a **Gold Standard** extraction pipeline for the Clinical AI Hackathon. It is a self-contained specification for an agent to implement a **Hybrid Architecture** that transforms semi-structured clinical Word documents into a structured, longitudinal Excel database.

This architecture replaces previous single-mode parsers by combining **Structural Document Parsing** (digital accuracy) with **Optical Character Recognition (OCR)** (visual layout awareness) to achieve maximum data integrity and clinical safety.

---

## Background and Motivation

Clinical MDT proformas are semi-structured, relying on visual cues (tables, bold headers, spatial alignment) that raw text parsers sometimes miss. By treating the document as both a structural object and a visual artifact, we achieve:

1.  **Layout Awareness:** Better handling of nested tables and "trapped" text in complex Word layouts.
2.  **Semantic Understanding:** Identifying clinical entities (e.g., "T3N1M0") as a "Staging" entity rather than just a string pattern.
3.  **Hybrid Verification:** Cross-verifying the **Digital Stream** (from `python-docx`) with the **Visual Stream** (from `PaddleOCR`). If Digital == Visual, we have 100% confidence. If not, the system flags it for review.
4.  **Robustness:** Handling variations in phrasing (e.g., "Chemo started" vs. "Initiated chemotherapy") through NLP models.

---

## Industry Standard Tech Stack

To ensure professional-grade results, the following libraries and tools are recommended:

- **Structural Parser:** `python-docx` for 100% character-perfect digital extraction from tables.
- **OCR Engine:** `PaddleOCR` (Baidu) or `DocTR` for layout-aware visual extraction and verification.
- **Clinical NER:** `MedSPaCy` (specialized clinical NLP) or `scispaCy` (`en_core_sci_lg` or `en_ner_bc5cdr_md`).
- **Data Handling:** `pandas` and `openpyxl` for Excel generation.
- **Intermediate Format:** `JSON` (for auditability and provenance).

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage0_setup_hybrid.py         # Model and dependency installation (Paddle, MedSPaCy)
│   ├── stage1_hybrid_extraction.py    # .docx + PaddleOCR -> fused.json
│   ├── stage2_clinical_ner_hybrid.py  # Fused JSON -> Clinical Entities (MedSPaCy)
│   ├── stage3_excel_assembly_hybrid.py # Entities -> .xlsx (with Styling)
│   └── pipeline_hybrid.py             # Orchestration
├── output/
│   ├── json_fused/                    # Per-case digital/visual fusion files
│   └── generated-database-hybrid.xlsx # Final Gold Standard output
```

---

## Implementation Details

### Stage 1: Hybrid Extraction & Fusion
1.  **Digital Pass:** Extract text from tables using `python-docx`. Preserves table/row indices.
2.  **Visual Pass:** Convert `.docx` pages to images and run **PaddleOCR** to extract text with spatial (X, Y) bounding boxes.
3.  **Fusion Engine:** Align digital text with visual coordinates. Ensure every block is tagged with its source table/row.
4.  **Verification:** Compare both streams. Mismatches must be recorded in JSON as `verification_discrepancy`.

### Stage 2: Named Entity Recognition (NER)
1.  **Entity Identification:** Use `MedSPaCy` to find:
    - `DIAGNOSIS` (Cancer type)
    - `STAGE` (TNM staging components: T, N, M, EMVI, CRM, PSW)
    - `PROCEDURE` (Endoscopy, Surgery)
    - `TREATMENT` (Chemotherapy agents, Radiotherapy)
2.  **Clinical Logic:** Use `ConText` for negation detection. "No metastases" must map to M0.
3.  **Normalization:** Map extracted entities to the canonical 88-column schema.

### Stage 3: Excel Assembly
1.  **Field Mapping:** Map entities to prototype columns.
2.  **Confidence Scoring:** Include an "AI Confidence" flag based on NER softmax and Hybrid match status.
3.  **Styling:** Copy fonts, colors, and row heights from `data/hackathon-database-prototype.xlsx`.

---

## Per-Stage Validation Strategy

### Stage 1 Validation: Hybrid Integrity
- **Objective:** Confirm Digital and Visual streams match.
- **Method:** Calculate Match Rate between `python-docx` strings and PaddleOCR strings.
- **Success Criteria:** 100% Match Rate for primary identifiers (NHS Number, MRN).

### Stage 2 Validation: NER Semantic Accuracy
- **Objective:** Confirm clinical entities were correctly categorized.
- **Method:** Compare output against a manually labeled "Gold Standard" for 5 cases.
- **Success Criteria:** F1-score > 0.95 for TNM and Dates.

### Stage 3 Validation: Assembly & Schema Consistency
- **Objective:** Confirm the final Excel matches the required clinical database format.
- **Method:** Run `validate_v4.py` against `data/hackathon-database-prototype.xlsx`.
- **Success Criteria:** 100% column alignment and zero "inferred" data without a corresponding flag.

---

## Engineering Constraints & Best Practices

1.  **Local Execution:** No cloud APIs. Use local PaddleOCR and Spacy models for DTAC/IG compliance.
2.  **Schema Enforcement:** Every entity must be validated against a JSON schema.
3.  **Provenance:** Keep `source_text` and `row_index` in the JSON to allow "click-to-source" verification.
4.  **Deterministic Fallbacks:** Use regex for stable patterns (NHS Numbers, DOB) to supplement NER.

---

## Validation and Benchmarking Strategy

### 1. Accuracy (Data Integrity)
- **Metric:** Character Error Rate (CER). Compare raw extraction against manual transcriptions.
- **Goal:** Minimize misreadings (e.g., "T3" as "I3").

### 2. Performance (Clinical Precision)
- **Metric:** Precision and Recall. 
- **Goal:** High precision to prevent hallucinations (incorrect cancer stages).

### 3. End-to-End Cell-Level Accuracy
- **Density Check:** Compare total non-empty cells (Target: > 700 cells) against the 675-cell baseline.
- **Fuzzy Match:** Use Levenshtein distance for long-prose fields (MDT Outcomes).

---

## Implementation Order

1.  **Environment Setup:** Install `paddleocr`, `paddlepaddle`, `medspacy`.
2.  **Hybrid Fusion:** Build the engine that aligns docx tables with OCR coordinates.
3.  **NER Implementation:** Configure `MedSPaCy` rules for TNM and Histology.
4.  **Assembly:** Integrate with `write_excel.py` logic.
5.  **Benchmarking:** Generate the final validation report.

---

## Author Attribution

This prompt was authored by Gemini CLI.
