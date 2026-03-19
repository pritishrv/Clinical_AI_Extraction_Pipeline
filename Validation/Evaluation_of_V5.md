# Evaluation of V5

## Overview

This document tracks the validation strategy and results for the v5 pipeline (`v5_VLM_LLM_DirectLogic`), which is the current state-of-the-art implementation. The pipeline uses a two-stage approach: Claude Vision (Stage 1) extracts raw clinical data from MDT Word documents into intermediate JSONs, and a hybrid LLM+deterministic mapper (Stage 2) populates the final Excel database.

The goal of validation is to answer: **how accurately does the pipeline extract and map clinical data from the source documents into the correct Excel fields?**

---

## Step 1: Ground Truth Strategy (Combined Approach)

### Why the Word Document is the Ground Truth

The `data/hackathon-database-prototype.xlsx` is a **schema template only** — it defines the column structure and formatting expectations but contains no patient data rows. The actual clinical data lives exclusively in `data/hackathon-mdt-outcome-proformas.docx`, which contains 50 synthetic, anonymised MDT cases.

Therefore, validation must trace back to the Word document as the authoritative source of truth.

```
hackathon-mdt-outcome-proformas.docx  (source of truth)
        |
                v
                  [v5 pipeline: Stage 1 + Stage 2]
                          |
                                  v
                                  hackathon_output_final.xlsx  (pipeline output)
                                          |
                                                  v
                                                    [validation: compare against source]
                                                    ```
nding row in `hackathon_output_final.xlsx`
- Compare field by field using:
  - **Exact match** for structured fields (MRN, NHS number, dates, TNM staging codes)
    - **Fuzzy match** (token sort ratio, threshold ≥ 85) for free-text fields (diagnosis, MDT outcome, clinical details)
    - Report: per-field accuracy, overall coverage (% non-empty cells), and a composite score

    **Weakness:** If Stage 1 made extraction errors, those errors will not be caught — we are validating Stage 2 mapping quality only.

    #### Layer B — Independent Docx Re-Parsing (Critical Fields)
    For a subset of 5–6 high-confidence, clearly-structured fields, we independently re-parse the `.docx` Gender
    5. MDT Meeting Date
    6. Primary Diagnosis (ICD-10 / tumour description)
    
    **Method:**
    - Parse `hackathon-mdt-outcome-proformas.docx` directly to extract these fields per patient
    - Compare against the corresponding cells in `hackathon_output_final.xlsx`
    - Flag any mismatches as potential hallucinations or mapping errors
    
    **Strength:** Fully independent of the pipeline — provides a true external audit for the most critical fields.
    
    ### Combined Scoring
    
    The two layers are combined into an overall Step 1 accuracy score:
    
    | Layer | Weight | Rationale |
    |---|---|---|
    | Layer A (JSON broad coverage) | 50% | Tests full field mapping across all 50 cases |
    | Layer B (Docx independent audit) | 50% | Tests ground truth fidelity for critical fields |
    
    ---
    
    *More steps will be added here as validation progresses.*file using `python-docx` and deterministic regex — completely bypassing the pipeline. This catches any hallucinations or errors introduced at Stage 1.

    **Fields selected for independent validation:**
    1. Patient MRN / Hospital Number
    2. NHS Number
    3. Date of Birth
    4.
                                                    ### The Combined Approach

                                                    Rather than relying on a single validation method, we use two complementary layers:

                                                    #### Layer A — JSON-Based Broad Coverage Validation
                                                    The intermediate JSONs in `v5_VLM_LLM_DirectLogic/output/json_raw_claude/` (case_000.json to case_049.json) represent Stage 1's extraction of the Word document — described by the pipeline author as "the same thing as the doc but in JSON." These serve as a fast, scalable proxy for the ground truth across all 50 cases and all fields.

                                                    **Method:**
                                                    - Load each `case_xxx.json` and the correspo
