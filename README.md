<img src="docs/digital_screen_1.jpg" alt="Clinical AI Hackathon" width="100%">

# Clinical-AI Extraction Pipeline: Automating Oncology MDT Records

[![Clinical AI](https://img.shields.io/badge/Domain-Healthcare%20AI-red.svg)](#)
[![Python](https://img.shields.io/badge/Language-Python%203.9+-blue.svg)](#)
[![Status](https://img.shields.io/badge/Status-Hackathon%20Baseline-success.svg)](#)

## 🩺 The Clinical Challenge
In modern oncology, **Multidisciplinary Team (MDT)** meetings are the gold standard for cancer treatment planning. However, the data captured during these sessions often remains "trapped" in semi-structured Word documents and fragmented systems like *Infoflex*. This creates a significant barrier for:
*   **Clinical Research:** Manually auditing thousands of patient records for longitudinal studies.
*   **Patient Outcomes:** Difficulty in tracking treatment efficacy across specific cancer cohorts.
*   **Operational Efficiency:** Clinicians spend hours manually re-entering data into research databases.

**Our Goal:** To develop a robust, AI-driven pipeline that transforms 50+ synthetic clinical MDT proformas into a structured, searchable, and longitudinal Excel database—aligning with NHS **Digital Technology Assessment Criteria (DTAC)**.

## 🚀 Technical Architecture
The system employs a multi-stage parsing strategy to extract high-fidelity clinical markers from complex medical narratives.

*   **Extraction Engine:** Leveraging Python (`python-docx`, `pandas`) and LLM-driven heuristics (Claude, Gemini, Codex) to identify TNM staging, imaging dates, and pathology findings.
*   **Normalization Logic:** Automated mapping of heterogeneous clinical terms (e.g., "CT Abdo/Pelvis", "CT CAP") to standardized database schemas.
*   **Validation Layer:** A regression-tested suite ensuring that extracted data points (like endoscopy dates and biopsy results) maintain 90%+ accuracy against clinician-verified ground truth.

## 📊 Performance Benchmarks
Our current baseline represents a state-of-the-art improvement over traditional regex-based extraction:

| Metric | Initial Baseline | Current Implementation (Team Version) |
| :--- | :--- | :--- |
| **Data Point Coverage** | 127 Cells | **675+ Cells** |
| **Extraction Accuracy** | ~66% | **~91%** |
| **Key Milestones** | Basic field detection | Advanced date inference & decision logic |

## 🛠 Tech Stack
*   **Languages:** Python
*   **Libraries:** `openpyxl` (Excel Styling), `pandas` (Data Transformation), `python-docx` (Word Parsing), `pytest` (Clinical Validation)
*   **Models:** Integrated API support for Anthropic Claude 3.5, Google Gemini Pro, and OpenAI Codex.
*   **Compliance:** Designed with **SaMD (Software as a Medical Device)** and **DCB0129/DCB0160** safety standards in mind.

## 📂 Repository Structure
```text
├── src/                      # Core extraction & normalization logic
├── data/                     # Synthetic proformas & Ground Truth datasets
├── tests/                    # Automated clinical validation suites
├── baseline-solution/        # Comparative analysis of AI-driven extraction attempts
├── docs/                     # Clinical specifications & regulatory considerations
└── HACKATHON_SUMMARY.md      # Executive summary of project impact
```

## 👥 The Team
This project was developed as part of the **Clinical AI Hackathon (March 2026)** by:
*   **[Your Name]** - [Your Role: e.g., Lead AI Engineer / Data Scientist]
*   **[Team Member Name]** - [Role]
*   **[Team Member Name]** - [Role]

*Special thanks to Dr. Anita Wale (St George’s University Hospitals NHS Foundation Trust) for the clinical problem statement and dataset.*

## 📈 Future Roadmap
*   **Treatment Specifics:** Improving extraction for complex Chemotherapy and Radiotherapy cycles.
*   **Pathology Detail:** Enhancing NLP models to capture secondary MRI results and histology nuances.
*   **FHIR Integration:** Moving from Excel to HL7 FHIR standards for direct EHR integration.

---
*This project is a prototype designed to demonstrate the feasibility of AI-assisted clinical data structured. It uses 100% synthetic, anonymized data.*
.
