# 06 OCR-NER Pipeline Prompt

Author: Gemini CLI

## Prompt Purpose

This prompt specifies a high-fidelity extraction pipeline that moves beyond deterministic regex-based parsing. It utilizes **Optical Character Recognition (OCR)** to handle document layout and **Named Entity Recognition (NER)** to extract clinical entities and key-value pairs.

The resulting data is stored in a structured **JSON** format before being assembled into the final **Excel** database.

---

## Background and Motivation

Clinical MDT proformas are often semi-structured, relying on visual cues (tables, bold headers, spatial alignment) that raw text parsers sometimes miss. By treating the document as a visual artifact (via OCR) and the content as a clinical language task (via NER), we achieve:

1.  **Layout Awareness:** Better handling of nested tables and "trapped" text in complex Word/PDF layouts.
2.  **Semantic Understanding:** Identifying "T3N1M0" as a "Staging" entity rather than just a string pattern.
3.  **Robustness:** Handling variations in phrasing (e.g., "Chemo started" vs. "Initiated chemotherapy") through NLP models.

---

## Industry Standard Tech Stack

To ensure professional-grade results, the following libraries and tools are recommended:

- **OCR Engine:** `pytesseract` (Tesseract) or `DocTR` (Document Text Recognition) for layout-aware extraction.
- **Clinical NER:** `MedSPaCy` (specialized clinical NLP) or `Hugging Face Transformers` with a `BioBERT` or `ClinicalBERT` backbone.
- **Data Handling:** `pandas` and `openpyxl` for Excel generation.
- **Intermediate Format:** `JSON` (for auditability and provenance).

---

## Architecture

```text
baseline-solution/
├── src/
│   ├── stage1_ocr_extraction.py      # .docx/PDF -> OCR Text -> Raw JSON
│   ├── stage2_clinical_ner.py        # Raw JSON -> NER Entities -> Normalized JSON
│   ├── stage3_excel_assembly.py      # Normalized JSON -> .xlsx
│   └── pipeline_ocr_ner.py           # Orchestration
├── models/                           # Local NER models or fine-tuning scripts
├── output/
│   ├── ocr_raw/                      # Raw text from OCR
│   ├── ner_processed/                # Entities and relationships in JSON
│   └── generated-database-ocr-ner.xlsx
```

---

## Implementation Details

### Stage 1: Document to OCR Text
1.  **Preprocessing:** Convert `.docx` pages to high-resolution images (using `pdf2image` or `python-docx2pdf`).
2.  **Layout Analysis:** Identify table boundaries and key headings (Demographics, Histology, etc.).
3.  **OCR Execution:** Run OCR on identified segments to extract raw text with spatial coordinates (bounding boxes).
4.  **Output:** A JSON object per case containing raw text segments and their location data.

### Stage 2: Named Entity Recognition (NER)
1.  **Entity Identification:** Use a clinical model (e.g., `en_core_sci_lg` or `medspacy`) to find:
    - `GPE` (Patient locations)
    - `DATE` (Clinical event dates)
    - `DIAGNOSIS` (Cancer type)
    - `STAGE` (TNM staging)
    - `PROCEDURE` (Endoscopy, Surgery)
    - `MEDICATION` (Chemotherapy agents)
2.  **Relation Extraction:** Use heuristics or models to link dates to procedures (e.g., "Colonoscopy" + "20/10/24").
3.  **Normalization:** Map extracted entities to the canonical schema required for the Excel output.
4.  **Output:** A `verified.json` file for each case, similar to the v2 architecture.

### Stage 3: Excel Assembly
1.  **Field Mapping:** Map the NER entities to the prototype columns.
2.  **Confidence Scoring:** Include an "AI Confidence" or "Human Review" column based on the NER model's softmax scores.
3.  **Styling:** Preserve the styling conventions from `write_excel.py`.

---

## Engineering Constraints & Best Practices

1.  **Local Execution:** Prioritize local models (MedSPaCy/Tesseract) over cloud APIs to ensure clinical data privacy.
2.  **Schema Enforcement:** Every NER-extracted entity must be validated against a predefined JSON schema before assembly.
3.  **Provenance:** Keep the `source_text` and bounding box coordinates in the JSON to allow "click-to-source" verification in the future.
4.  **Deterministic Fallbacks:** Use regex for highly stable patterns (like NHS Numbers) to supplement the NER model.

---

## Implementation Order

1.  **Environment Setup:** Install Tesseract, Spacy, and MedSPaCy.
2.  **OCR Pipeline:** Build `stage1_ocr_extraction.py` and verify text recovery from table cells.
3.  **NER Implementation:** Configure `MedSPaCy` to recognize the specific cancer markers (TNM, Histology).
4.  **JSON Mapping:** Define the transformation logic from NER spans to the 88-column Excel schema.
5.  **Assembly:** Integrate with the existing `write_excel.py` logic.

---

## Author Attribution

This prompt was authored by Gemini CLI.
