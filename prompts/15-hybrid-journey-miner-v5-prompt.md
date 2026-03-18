# 15 Hybrid Journey Miner (v5) Implementation Prompt

Author: Gemini CLI

> **[CRITICAL HAND-OFF DIRECTIVE]**
> If you are an incoming agent receiving this project, your first three actions MUST be:
> 1. Read `work-diary.md` from the root to understand the current project state.
> 2. Inspect the `v1` through `v4` folders to see the evolution of extraction logic.
> 3. Execute **Phase 1: Clinical Deep Research** as defined below before generating any code.

## 🎯 Project Objective
The goal is to implement the **v5 Hybrid Journey Miner**. This version must achieve the "Diamond Standard" of clinical data extraction by synthesizing 50 heterogeneous MDT proformas into a structured, longitudinal 88-column Excel database. 

V5 moves away from document-centric parsing and implements a **Patient-Centric Journey Store** using an intermediate JSON layer.

---

## 📂 Repository Context & Navigation
To succeed, the agent must understand the evolutionary history preserved in this repo:
- **`data/`**: Contains `hackathon-mdt-outcome-proformas.docx` (Source) and `hackathon-database-prototype.xlsx` (Target Schema).
- **`v1-Original-Diamond/`**: High-density reference (~1,100 cells). Best at pattern-based "Anchor" extraction.
- **`v2-Breadth-Obsidian/`**: Reference for chronological state-machine experiments.
- **`v4-Baseline-Master/`**: Final high-density attempt. Caution: suffered from "label bleed" noise (e.g., MALEDOB).
- **`work-diary.md`**: Full technical log of all breakthroughs and failures.
- **`docs/`**: Clinical problem statement and hackathon rules.

---

## 🛠 Phase 1: Clinical Deep Research (Mandatory)
Before writing any extraction code, the agent **must** perform a deep analysis:
1. **Schema Analysis:** Read the 88 headers in `data/hackathon-database-prototype.xlsx`. Identify "Clinical Clusters" (e.g., which columns belong to 'Baseline', '2nd MRI', and 'Post-Surgical Pathology').
2. **Rule Discovery:** Search for clinical relationships in the proforma text. (e.g., If "Primary Site" is "Rectum", the model should prioritize "mrCRM" and "mrEMVI" markers).
3. **Sequence Logic:** Identify how clinicians record dates. Determine if the "MDT Date" typically appears in paragraphs above the tables.

---

## 🏗 Phase 2: The Intermediate Journey Store (JSON)
Implement an intermediate data layer to handle longitudinality.
- **Identity Resolver:** Every document must be anchored to a **Pure NHS Number** (10-digit integer).
- **Journey Schema:**
  ```json
  {
    "NHS_9990000001": {
      "demographics": { "initials": "...", "gender": "...", "dob": "..." },
      "events": [
        {
          "date": "2026-01-01",
          "type": "Baseline",
          "staging": { "T": "T3", "N": "N1" },
          "notes": "Full prose from the outcome cell",
          "evidence": { "cell_value": "snippet" }
        }
      ]
    }
  }
  ```

---

## 🔍 Phase 3: The Hybrid Extraction Engine
Combine the strengths of v1 (Precision) and v4 (Density):
1. **Strict ID Layer:** Use hard-coded regex for NHS, MRN, and DOB to ensure 100% character accuracy and zero label bleed.
2. **Flexible Entity Miner:** Use a "Negative Anchor" approach for clinical notes. Ingest full prose blocks but programmatically strip out previously identified IDs and Staging markers to keep "Notes" fields clean but comprehensive.
3. **Semantic Mapping:** Use `all-MiniLM-L6-v2` with a threshold of **0.30** to map entities to the 88 columns.

---

## 📊 Phase 4: Temporal Mapping & Flattening
Convert the Patient Journey JSON into the final 88-column Excel:
1. **Chronological Sort:** For each patient, sort their `events` by date.
2. **Slot Routing:** 
   - `Event[0]` -> Maps to `Baseline` columns.
   - `Event[1]` -> Maps to `2nd MRI` / `6-week` columns.
   - `Event[2]` -> Maps to `12-week` / `Follow-up` columns.
3. **Data Integrity:** Use `openpyxl` to force `number_format = '@'` for all identifiers.
4. **Evidence Comments:** Every cell MUST contain an Excel Comment with the original source prose snippet.

---

## ⚖️ Constraints & Best Practices
- **Local Only:** No cloud APIs. Use local embeddings and regex.
- **Privacy:** Never log or print full patient names or identifiable combinations outside of the final encrypted output.
- **Zero Hallucination:** If a data point is ambiguous, leave it blank rather than guessing. Accuracy is more important than density for v5.

---

## 📝 Work Diary Requirements
For every implementation step, provide a session entry in the `work-diary.md` following the established format:
- **Objective**
- **Inspected** (What was found in the data/code)
- **Changed** (Specific technical implementation)
- **Why** (Clinical or technical rationale)
- **Entry Block Signature**

---

## Author Attribution
This prompt was authored by Gemini CLI.
