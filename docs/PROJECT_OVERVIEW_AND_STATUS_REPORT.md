# Clinical AI Hackathon: Project Overview and Status Report

## 1. Problem Statement
Multidisciplinary Team Meetings (MDTs) are critical for cancer treatment planning in the NHS. However, the current process for capturing patient data is manual and inconsistent. Data is often circulated as Word documents, making it difficult to extract structured information for audits, research, or long-term clinical tracking.

**The Goal:** Automate the extraction of clinical history, staging (TNM), imaging, and pathology data from semi-structured MDT documents into a structured, searchable database (Excel).

## 2. Judge Panel
The following experts will evaluate the hackathon outcomes:
- **[Dr. Anita Wale](https://www.stgeorges.nhs.uk/people/dr-anita-wale/)**: Consultant Radiologist and Clinical Academic at St George’s University Hospitals NHS Foundation Trust.
- **[Dr. Alex Nicholls](https://uk.linkedin.com/in/alex-nicholls-57301a38)**: Ministry of Defence.
- **[Hitesh Patel](https://uk.linkedin.com/in/hitesh-patel-68ab0223a)**: Superintendent Radiographer and Radiology IT Systems (RITS) Manager at St George’s University Hospitals NHS Foundation Trust.

## 3. Dataset and Objectives
- **Input:** `data/hackathon-mdt-outcome-proformas.docx` (50 synthetic, anonymized MDT cases).
- **Target Output:** `data/hackathon-database-prototype.xlsx` (A longitudinal patient database).
- **Success Criteria:** High coverage and accuracy of extracted data, matching the clinician-provided prototype.

## 3. Repository Architecture
The repository is organized to support a multi-stage development and evaluation lifecycle:

- **`data/`**: Contains the synthetic input documents and the "ground truth" Excel prototype.
- **`baseline-solution/`**: A working implementation with three distinct iterations:
    - **Gemini Attempt**: Initial pipeline setup and basic field extraction.
    - **Codex Attempt**: Improved cell coverage (661 non-empty cells) and Excel styling.
    - **Claude Code Attempt**: Current state-of-the-art (675 non-empty cells) with advanced date inference and decision logic.
- **`src/`**: Python source code for the extraction pipeline (`python-docx`, `pandas`, `openpyxl`).
- **`docs/`**: Clinical specifications, regulatory considerations (DTAC, SaMD), and meeting minutes.

## 4. Current Implementation Status
The project has evolved through three AI-driven iterations, each improving data extraction density:

| Metric | Gemini | Codex | Claude Code |
| :--- | :--- | :--- | :--- |
| **Non-empty Cells** | 127 | 661 | 675 |
| **Normalized Match** | 8/12 | 10/12 | 11/12 (est.) |

### Key Improvements:
- **Date Extraction**: Enhanced patterns for endoscopy and histology biopsy dates.
- **Broadening Scope**: Improved detection of CT imaging variants (Abdomen, Pelvis, etc.).
- **Decision Logic**: Automated extraction of MDT outcomes after specific labels.

## 5. Outstanding Challenges & Gaps
Despite progress, several high-value clinical fields remain under-populated:
- **Treatment Specifics**: Chemotherapy, radiotherapy, and immunotherapy fields are mostly empty.
- **Pathology Detail**: Specific histology biopsy dates (g) and second MRI results.
- **Reliability**: Some fields rely on heuristics that may not scale to all 50 cases without further refinement.

## 6. Technical Stack
- **Languages**: Python 3.x
- **Libraries**: `python-docx`, `pandas`, `openpyxl`, `pytest`
- **AI Integration**: Custom prompts and wrappers for Google Gemini, OpenAI Codex, and Anthropic Claude.

---
*Report generated on Tuesday, March 17, 2026.*
