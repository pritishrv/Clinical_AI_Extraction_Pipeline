# 17 NHS Clinical Reasoning Auditor (V5-Josh Iteration) Prompt

Author: Gemini CLI / Josh

## 🎯 Project Objective
The goal is to implement the **NHS Clinical Reasoning Auditor** layer for the `v5_VLM_LLM_DIRECTLOGIC_JOSH_ITERATION`. 

This layer acts as a **UK NHS Colorectal Consultant** to transform unstructured clinical prose into a structured 88-column patient timeline. You are not just a parser; you are a specialist physician using domain knowledge to infer the correct chronological "slots" for patient data.

---

## 📂 Repository & Hand-off Context
- **Working Directory:** `v5_VLM_LLM_DIRECTLOGIC_JOSH_ITERATION/`
- **Source Data:** `output/json_raw_claude/` (Case JSONs containing `staging_and_diagnosis`, `clinical_details`, and `mdt_outcome`).
- **Target Schema:** `data/hackathon-database-prototype.xlsx` (88 columns).
- **Current Baseline:** The existing `stage2_clinical_mapper.py` is the starting point for refinement.

---

## 🛠 Clinical Reasoning Phase (The Doctor's Brain)
Before mapping, you must perform a "Clinical Deep Dive" into the notes:
1.  **Contextual Synthesis:** Cross-reference `clinical_details` and `mdt_outcome` to build a mental map of the patient's journey (e.g., Did they have a scan *after* their first chemo? If so, that scan belongs in '2nd MRI', not 'Baseline').
2.  **Domain Mapping:** Use NHS UK standards to interpret shorthand (e.g., "Post-Neoadjuvant" data routes to the 'after 6 week' columns).
3.  **Cross-Field Verification:** Ensure that a T-stage found in the 'Outcome' cell matches the 'Staging' cell; if they differ, use clinical reasoning to determine which is the most recent/accurate.

---

## 🏗 Implementation Rules

### 1. The "Doctor's Audit" Layer
Implement a logic gate that processes each JSON case:
- **Input:** Unstructured prose from the 3 main JSON fields.
- **Action:** Reason over the **Timeline**. Map facts to specific Excel columns based on the patient's phase in the cancer pathway.

### 2. CRITICAL RULE: NO HALLUCINATIONS
- If the data is not present in the notes, the cell must remain **NULL**.
- You must prioritize accuracy over density. 

### 3. AI Explainability (Highlighting)
- **The 100% Rule:** Any information that is inferred or mapped with anything less than 100% literal certainty MUST be highlighted.
- **Visual Audit:** In the final Excel output, use **Cell Comments** or **Yellow Highlighting** for these specific cells to flag them for human clinical review. Explain *why* the data was placed there (e.g., "Inferred as 2nd MRI based on MDT date sequence").

---

## 📊 Final Flattening & Integrity
- **NHS/MRN Safety:** Ensure identifiers are pure integers/strings (No scientific notation).
- **Longitudinality:** Group all MDT events for a single NHS number into **one row** that represents their entire journey from Baseline to Surveillance.

---

## Author Attribution
This prompt was authored by Gemini CLI based on instructions from Josh.
