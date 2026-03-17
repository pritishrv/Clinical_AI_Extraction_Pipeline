# 03 Deep Research Prompt

Author: Claude Code

## Prompt Purpose

Give this prompt verbatim to an online AI agent (ChatGPT, Claude.ai, Grok, or similar) to
generate a domain-knowledge report on colorectal cancer MDT clinical practice.

The resulting report should be saved locally as:

```
baseline-solution/reports/deep-research-<agent>.md
```

For example:
- `deep-research-chatgpt.md`
- `deep-research-claude.md`
- `deep-research-grok.md`

Once the reports are saved locally, Claude Code will consolidate them into a participant-facing
orientation document.

---

## Prompt

You are a clinical domain expert and science communicator. I am a software engineer or data
scientist participating in a clinical AI hackathon focused on colorectal cancer MDT
(Multidisciplinary Team) decision-making. I have no clinical background.

Please produce a comprehensive, well-structured research report that will help me and my
teammates:

1. Understand colorectal cancer: what it is, how it develops, how it is classified
2. Understand how it is detected and staged
3. Understand the treatment pathways and how MDT decisions are made
4. Understand the terminology, acronyms, and abbreviations clinicians use day to day
5. Understand the data artefacts we are likely to encounter (imaging reports, pathology reports,
   MDT proformas, endoscopy notes)

The report should be thorough enough that a technically competent non-clinician can read it once
and then hold a meaningful conversation with a colorectal cancer clinician, ask sensible questions,
and understand the answers.

---

### Section 1: What Is Colorectal Cancer?

Cover:
- Anatomy: colon and rectum, their segments, clinical significance of location (right colon,
  left colon, rectum, sigmoid, caecum, ascending, transverse, descending)
- How colorectal cancer develops (adenoma-carcinoma sequence, polyp types)
- Epidemiology: incidence, risk factors, screening rationale
- Histological subtypes: adenocarcinoma, mucinous, signet ring, other variants
- Differentiation grades: well, moderate, poorly differentiated
- ICD-10 codes relevant to colorectal cancer (C18, C19, C20 etc.)

---

### Section 2: Detection and Investigation

Cover:
- Symptoms that trigger investigation and the TWR / DTT / 2WW pathway (explain these acronyms)
- Endoscopy types used:
  - Colonoscopy (complete vs incomplete)
  - Flexi-sigmoidoscopy (flexi sig)
  - Rigid sigmoidoscopy
  - CT colonography (virtual colonoscopy)
  - What "tattoo" means in an endoscopy report
  - What "ICV" (ileocaecal valve) means and why reaching it matters
- Biopsy and histopathology:
  - What a biopsy report contains
  - Differentiation grade
  - MMR (Mismatch Repair) status — explain MMR deficient vs proficient and why it matters
  - MSI (Microsatellite Instability) and its relationship to MMR
  - IHC (Immunohistochemistry) testing
  - KRAS, NRAS, BRAF mutation testing and clinical relevance
- Blood tests:
  - CEA (Carcinoembryonic Antigen): what it is, normal range, clinical use, limitations

---

### Section 3: Staging

Cover:
- TNM staging system in detail:
  - T stage (T0 through T4, substages a/b/c, sm1/sm2/sm3 for early lesions)
  - N stage (N0 through N2, substages)
  - M stage (M0, M1a/b/c)
  - Prefixes: c (clinical), p (pathological), mr (MRI-based), y (post-treatment), r (recurrent)
- Dukes staging (A/B/C/D) — historical context, why it still appears
- Integrated TNM stage groupings (Stage I through IV)
- Specific MRI staging parameters for rectal cancer:
  - mrT, mrN (explain difference from clinical T and N)
  - CRM (Circumferential Resection Margin) — what it is, clear vs threatened vs involved, why it matters
  - EMVI (Extramural Vascular Invasion) — what it is, positive vs negative, clinical significance
  - ISP (Intersphincteric Plane) — what it is and why it matters for surgery
  - PSW (Posterior Surgical Wall / Presacral Space) — explain
  - Low / mid / upper rectal tumour — how distance from anal verge affects treatment
- Difference between colon cancer staging and rectal cancer staging (why rectal cancer has more
  MRI-specific parameters)

---

### Section 4: Imaging Modalities

Cover:
- CT (Computed Tomography):
  - CT TAP (Thorax, Abdomen, Pelvis) — standard staging scan
  - CT abdomen/pelvis
  - CT colonography
  - What to expect in a CT staging report for colorectal cancer
  - Incidental findings: what they are and why they matter
  - Metastatic disease patterns (liver, lung, peritoneum, lymph nodes)
- MRI (Magnetic Resonance Imaging):
  - Why MRI is preferred for rectal cancer staging
  - MRI pelvis / MRI rectum — what these mean
  - High-resolution rectal MRI protocol
  - What "low signal" means on MRI and clinical significance (e.g. post-treatment)
  - Response assessment MRI after neoadjuvant treatment
  - 6-week MRI and 10-week MRI post-CRT
  - 12-week MRI
- PET-CT (Positron Emission Tomography CT):
  - What FDG-avid means
  - When PET-CT is used in colorectal cancer
  - Difference between PET-CT and standard CT
- Ultrasound:
  - ERUS (Endorectal Ultrasound) — when used, what it shows

---

### Section 5: MDT (Multidisciplinary Team) Process

Cover:
- What an MDT is: who attends (colorectal surgeon, oncologist, radiologist, pathologist,
  gastroenterologist, CNS nurse, MDT coordinator), what decisions are made
- MDT proforma: what it is, what fields it typically contains
- The flow from referral to MDT discussion to treatment decision
- What "rediscuss at MDT" means and why a case comes back
- MDT outcome categories (what decisions an MDT typically makes)
- Cancer target dates:
  - 62-day target: what it is, why it matters
  - DTT (Decision to Treat): what this means
  - TWR (Two-Week Rule / Two-Week Wait): what triggers it
- BCSP (Bowel Cancer Screening Programme): what it is and how it feeds into MDT

---

### Section 6: Treatment Pathways

Cover each treatment modality in enough depth for a non-clinician to understand:

#### Surgery
- Types of surgery for colon cancer:
  - Right hemicolectomy
  - Left hemicolectomy
  - Sigmoid colectomy
  - Anterior resection (AR)
  - Hartmann's procedure
  - Subtotal / total colectomy
- Types of surgery for rectal cancer:
  - Anterior resection (low / ultra-low)
  - ELAPE (Extralevator Abdominoperineal Excision) — explain
  - APE / APER (Abdominoperineal Excision of Rectum)
  - TME (Total Mesorectal Excision) — what it is, why it is the gold standard
  - Local excision options: TEM (Transanal Endoscopic Microsurgery), TAMIS, Papillon
  - Defunctioning stoma / temporary stoma
- Surgical review: what it means when the MDT says "refer for surgical review"
- Tattooing: why surgeons ask for endoscopic tattoo before surgery

#### Radiotherapy
- Long-course CRT (Chemoradiotherapy): fractions, duration, concurrent chemotherapy agent
- Short-course RT (SCRT): fractions, timing relative to surgery
- EBRT (External Beam Radiotherapy): what it is
- Papillon (contact radiotherapy / endocavitary radiation): what it is, when used
- Response to radiotherapy: complete response (CR), near-complete response, partial response
- Watch and Wait (W&W): what it means, which patients qualify, surveillance protocol, risks

#### Chemotherapy
- FOXTROT trial and FOXTROT regimen: explain what this is and why it appears in MDT notes
- FOLFOX: components (5-FU, oxaliplatin, leucovorin), what it is used for
- FOLFIRI: components, use
- CAPOX / XELOX: components (capecitabine, oxaliplatin), oral vs IV distinction
- Capecitabine (Xeloda): oral fluoropyrimidine, role in CRT
- Neoadjuvant chemotherapy: what "downstaging" means
- TNT (Total Neoadjuvant Therapy): explain the concept
- Adjuvant chemotherapy: when given, rationale

#### Targeted Therapy and Immunotherapy
- Anti-EGFR agents (cetuximab, panitumumab): when used, KRAS/RAS requirement
- Anti-VEGF agents (bevacizumab): mechanism, use
- Immunotherapy (pembrolizumab, nivolumab): role in MSI-H / MMR-deficient colorectal cancer
- When immunotherapy replaces chemotherapy

#### Local Treatments for Metastatic Disease
- Liver resection for colorectal liver metastases
- SIRT (Selective Internal Radiation Therapy) / radioembolisation
- SABR (Stereotactic Ablative Radiotherapy)
- Ablation techniques (RFA, microwave)

---

### Section 7: Pathway Summaries

Provide a plain-English walkthrough of the typical treatment pathway for:

1. A patient with early colon cancer (T1/T2, N0, M0) — straight to surgery
2. A patient with locally advanced rectal cancer (T3/T4, CRM threatened) — neoadjuvant CRT,
   restaging MRI, then surgery
3. A patient with metastatic colorectal cancer (M1) — systemic chemotherapy, MDT discussion
   of resectability
4. A rectal cancer patient suitable for Watch and Wait after complete clinical response

---

### Section 8: Glossary of Acronyms and Abbreviations

Provide an alphabetically sorted glossary of every acronym, abbreviation, and clinical shorthand
that appears in this report or that would typically appear in colorectal cancer MDT documentation.

For each entry provide:
- The expansion
- A one-sentence definition

Include at minimum: APE, AR, AR (anterior resection), BCSP, BRAF, BSC, CAR, CAPOX, CEA, CNS,
CR, CRM, CRT, CT, DTT, EBRT, EGFR, ELAPE, EMVI, ERUS, FDG, flexi sig, FOLFIRI, FOLFOX,
FOXTROT, 5-FU, HER2, ICD-10, ICV, IHC, ISP, KRAS, MDT, MMR, MRI, mrCRM, mrEMVI, mrN, mrT,
MSI, MSI-H, N stage, nCRT, NRAS, PET-CT, PR, PSW, RAS, RFA, SABR, SCRT, SIRT, SM1/SM2/SM3,
T stage, TAMIS, TEM, TME, TNM, TNT, TWR, VEGF, W&W, 2WW, 62-day target.

---

### Output Format Requirements

- Use clear Markdown headings and subheadings matching the sections above.
- Use bullet points or numbered lists within sections for scannability.
- Bold key terms on first use.
- Where a concept has a common synonym or abbreviation, state both.
- Do not truncate. Produce the full report even if it is long.
- End with a Sources section citing the guidelines, papers, or databases you drew on
  (NICE guidelines, BSG guidelines, ACPGBI, ESMO, NCCN, RCR, relevant Lancet / NEJM papers
  for FOXTROT, RAPIDO, PRODIGE, CAO/ARO/AIO, ARISTOTLE, MERCURY trials etc.).

---

## After You Have the Reports

Save each agent's response as a Markdown file in:

```
baseline-solution/reports/deep-research-<agent>.md
```

Then return to Claude Code and run:

```
action @prompts/03-deep-research-prompt.md
```

Claude Code will read all available `deep-research-*.md` files and produce a consolidated
participant orientation document at:

```
baseline-solution/reports/participant-orientation.md
```

## Author Attribution

This prompt was authored by Claude Code.
