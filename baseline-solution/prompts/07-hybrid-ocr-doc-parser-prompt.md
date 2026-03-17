# 07 Hybrid OCR and Structural Parser Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies a **Gold Standard** extraction pipeline that replaces the single-mode parsers with a **Hybrid Architecture**:

1.  **Stage 1** — `.docx` → `fused.json` (Hybrid Digital + Visual Extraction)
2.  **Stage 2** — `fused.json` → `entities.json` (Ensemble Clinical NER)
3.  **Stage 3** — `entities.json` → `.xlsx` (High-Fidelity Assembly)

It combines **python-docx** (100% digital accuracy) with **PaddleOCR** (visual verification) to maximize clinical safety and data density.

---

## Background and Motivation

Clinical MDT proformas often contain data that is visually apparent to a human but structurally complex for a machine (e.g., text in embedded images or complex nested tables).

- **Digital Parsing** is fast and character-perfect but can be blind to visual layout changes.
- **OCR (Visual Parsing)** understands layout but can introduce character errors (e.g., "T3" misread as "I3").

The **Hybrid Approach** cross-verifies both streams. If the digital and visual texts match, we have high confidence. If they differ, the system flags the field for human review. This is the only defensible way to automate oncology data extraction at scale.

---

## Design Decisions (Agreed Before Implementation)

### Decision 1: Hybrid Cross-Verification is Mandatory
Every high-stakes field (NHS Number, TNM Stage, Dates) must be extracted by both the structural parser and the OCR engine. Discrepancies must be recorded in the `source_evidence` of the JSON and flagged in the final Excel output.

### Decision 2: Local Execution Only (Data Privacy)
To comply with NHS data governance (DTAC), the pipeline must use only local models. This implementation uses **PaddleOCR** and **MedSPaCy** running on local compute. No patient data is sent to cloud APIs.

### Decision 3: Use of Clinical Negation Detection
We must distinguish between "metastases" and "no metastases." The pipeline must use MedSPaCy's `ConText` component to identify negation modifiers. An entity marked as `negated=True` must be mapped correctly (e.g., "No metastases" → M0).

### Decision 4: Provenance and Confidence Flags
The final Excel workbook must include a `Human Verification Required` column. This column must detail *why* a review is needed (e.g., "OCR mismatch," "Low NER confidence," or "Inferred date").

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage0_setup_hybrid.py         # Model and dependency installation
│   ├── stage1_hybrid_extraction.py    # .docx + PaddleOCR -> fused.json
│   ├── stage2_clinical_ner_v4.py      # Fused JSON -> Clinical Entities
│   ├── stage3_excel_assembly_v4.py    # Entities -> .xlsx
│   └── pipeline_v4_hybrid.py          # Orchestrator
├── output/
│   ├── json_fused/                    # Intermediate fusion files
│   └── generated-database-hybrid.xlsx # Final Gold Standard output
└── tests/
    ├── test_hybrid_fusion.py
    └── test_clinical_ner_accuracy.py
```

---

## Implementation Order

1.  **Stage 0: Setup**: Install `paddleocr`, `paddlepaddle`, `medspacy`.
2.  **Stage 1: Fusion**: Implement the logic that aligns `python-docx` table cells with PaddleOCR visual bounding boxes.
3.  **Stage 2: NER**: Implement the MedSPaCy ensemble with custom rules for TNM and treatments.
4.  **Stage 3: Assembly**: Map the entities to the 88-column schema, ensuring the "Verification Required" logic is robust.
5.  **Validation**: Compare density and accuracy against the prototype.

---

## Author Attribution

This prompt was authored by Gemini CLI.
