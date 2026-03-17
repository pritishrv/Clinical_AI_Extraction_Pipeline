# Colorectal Cancer Primer for Clinical AI Hackathon Participants

**Audience:** Software engineers and data scientists with no clinical background.
**Purpose:** Give you enough domain knowledge to read the MDT proforma data, understand what clinicians are describing, and ask informed questions.
**Reading time:** 45–60 minutes.

**Source reports consolidated here:**
- `deep-research-grok.md` (Grok)
- `deep-research-gemini.docx` (Gemini)
- `deep-research-claude.docx` (Claude.ai)

---

## Section 1: What Is Colorectal Cancer?

### Anatomy

The **large intestine** (large bowel) is the final ~1.5 m of the gastrointestinal tract. It is divided into:

| Segment | Location | Clinical note |
|---------|----------|---------------|
| **Caecum** | Bottom-right abdomen | Where the small bowel joins via the **ileocaecal valve (ICV)**. Cancers here grow silently (wide lumen, liquid stool). |
| **Ascending colon** | Right side, upward | Right-sided cancers tend to cause iron-deficiency anaemia rather than obstruction. |
| **Hepatic flexure** | Upper right (near liver) | Bend between ascending and transverse. |
| **Transverse colon** | Crosses upper abdomen | Most mobile segment. |
| **Splenic flexure** | Upper left (near spleen) | Poor blood supply; technically challenging for surgery. |
| **Descending colon** | Left side, downward | Left-sided cancers cause bowel habit change and visible bleeding earlier (more formed stool). |
| **Sigmoid colon** | S-shaped, lower left | Common cancer site; prone to diverticular disease too. |
| **Rectum** | Last 12–15 cm, in pelvis | Surrounded by the **mesorectum** (fat + lymph nodes wrapped in mesorectal fascia). Rectal cancer is staged and treated differently from colon cancer because of its position in the narrow bony pelvis. |

### How Colorectal Cancer Develops

Most CRC follows the **adenoma-carcinoma sequence**: normal lining → benign polyp (adenoma) → cancer, over 10–15 years through accumulated genetic mutations (APC → KRAS → TP53).

Key polyp types:
- **Adenomas** — tubular, villous, tubulovillous; precancerous
- **Sessile serrated lesions (SSL)** — flat, easy to miss at endoscopy; associated with BRAF mutation and MSI-H tumours
- **Hyperplastic polyps** — usually benign, no malignant potential

### Histological Subtypes

- **Adenocarcinoma** — 95% of cases; originates from glandular epithelium
- **Mucinous adenocarcinoma** — >50% mucin; poorer response to chemoradiotherapy
- **Signet ring cell carcinoma** — very aggressive; cells look like signet rings on microscopy

### Differentiation Grade (How Aggressive the Tumour Looks)

| Grade | What it means |
|-------|--------------|
| **Well differentiated (G1)** | Looks like normal colon glands; lower metastatic risk |
| **Moderately differentiated (G2)** | Most common |
| **Poorly differentiated (G3)** | Disorganised cells; high lymph node spread risk |

### ICD-10 Codes (You Will See These in the Data)

| Code | Meaning |
|------|---------|
| C18.0–C18.9 | Colon cancer (subsite coded: .0 = caecum, .2 = ascending, .7 = sigmoid, etc.) |
| C19 | Rectosigmoid junction |
| C20 | Rectum |

---

## Section 2: Detection and Investigation

### Referral Pathway

When a patient presents with symptoms (rectal bleeding, change in bowel habit, weight loss, anaemia), they are referred urgently via the **Two-Week Wait (2WW / TWR)** pathway — the GP must ensure a specialist appointment within 14 days.

The **Bowel Cancer Screening Programme (BCSP)** sends a **FIT (Faecal Immunochemical Test)** kit to people aged 50–74 every 2 years. A positive FIT result triggers a colonoscopy referral and entry into the MDT pathway.

### Endoscopy Types

| Procedure | What it does | Key term |
|-----------|-------------|----------|
| **Colonoscopy** | Camera on flexible tube; examines whole large bowel from rectum to caecum | "Complete" = reached the **ICV**; incomplete = follow-up CT colonography needed |
| **Flexible sigmoidoscopy (flexi sig)** | Examines rectum and sigmoid (~60 cm); quicker, less prep | Misses right-sided lesions |
| **Rigid sigmoidoscopy** | Short rigid instrument; clinic-based; used to measure exact distance of rectal tumour from **anal verge** | "8 cm from anal verge" = measurement this gives |
| **CT colonography (CTC)** | "Virtual colonoscopy"; CT scan with air inflation; used if colonoscopy incomplete or patient too frail | |

**Endoscopic tattoo:** When a lesion is found that will need surgery, the endoscopist injects ink (India ink) near it. Surgeons performing keyhole (laparoscopic) surgery have no sense of touch, so the tattoo tells them exactly where to resect. Without it, the wrong bowel segment could be removed.

### Biopsy and Histopathology

A biopsy confirms whether cancer is present and provides critical molecular information:

- **Histological type and differentiation grade** (as above)
- **MMR status** — see below
- **RAS/BRAF mutations** — relevant only in metastatic disease; determines eligibility for targeted therapy

#### MMR and MSI Status — Critical Concept

The **Mismatch Repair (MMR)** system consists of four proteins (MLH1, MSH2, MSH6, PMS2) that proofread DNA copying errors.

| Status | Meaning | Clinical impact |
|--------|---------|----------------|
| **dMMR** (deficient MMR) | One or more proteins absent (detected by IHC staining) | Tumour is **MSI-H**; eligible for immunotherapy; may not benefit from 5-FU chemotherapy; young patient → screen for Lynch syndrome |
| **pMMR** (proficient MMR) | All proteins present; DNA stable (**MSS** = microsatellite stable) | Most CRCs (~85%); standard chemotherapy applies |

**MSI-H** = **microsatellite instability high** — the molecular consequence of dMMR. You will see both terms used interchangeably in clinical notes.

#### Tumour Marker: CEA (Carcinoembryonic Antigen)

A blood protein produced by many colorectal cancers. Normal: <5 ng/mL (non-smokers). Not used for screening (too non-specific), but valuable for:
- Monitoring response to treatment (should fall)
- Surveillance post-surgery — a rising CEA is often the first sign of recurrence

---

## Section 3: Staging

### The TNM System

Every MDT discussion is framed in TNM (Tumour, Node, Metastasis) staging — 8th Edition.

#### T Stage (Primary Tumour Depth)

| Stage | Meaning |
|-------|---------|
| Tis | Carcinoma in situ (mucosa only) |
| T1 | Into submucosa |
| T1 sm1/sm2/sm3 | Early lesions subdivided by submucosal invasion depth; sm3 → usually needs formal surgery rather than local excision |
| T2 | Into muscularis propria (main muscle layer) |
| T3 | Through muscularis into surrounding fat |
| T4a | Through outer lining (peritoneum) |
| T4b | Into adjacent organs (e.g., bladder) |

#### N Stage (Lymph Nodes)

| Stage | Meaning |
|-------|---------|
| N0 | No lymph node involvement |
| N1a | 1 node |
| N1b | 2–3 nodes |
| N1c | Tumour deposits in fat, no discrete nodes |
| N2a | 4–6 nodes |
| N2b | ≥7 nodes |

#### M Stage (Distant Spread)

| Stage | Meaning |
|-------|---------|
| M0 | No metastases |
| M1a | One distant organ (e.g., liver only) |
| M1b | Multiple organs |
| M1c | Peritoneum ± others |

#### Staging Prefixes

You will always see a prefix in MDT notes:

| Prefix | Meaning |
|--------|---------|
| **c** | Clinical — based on imaging before any treatment |
| **p** | Pathological — based on examination of the surgical specimen |
| **mr** | MRI-based — used specifically for rectal cancer |
| **y** | Post-neoadjuvant treatment (e.g., **ypT2N0** = stage after chemo/radiotherapy) |
| **r** | Recurrent disease |

Example: `ycT1N0M0` = staging by imaging (y = post-treatment, c = clinical) of T1N0M0 disease.

#### Integrated Stage Groups

Stage I (T1–2 N0 M0) → Stage IV (any T any N M1). Stage I–II = localised; Stage III = nodes involved; Stage IV = metastatic.

#### Dukes Staging (Historical)

Still appears in older notes: Dukes A = Stage I, B = Stage II, C = Stage III, D = Stage IV. Replaced by TNM but not gone.

---

### MRI-Specific Parameters for Rectal Cancer

Rectal cancer gets a much more detailed staging MRI than colon cancer, because the surgical goal is to remove the tumour within clear margins without damaging the sphincters or pelvic nerves.

| Parameter | What it is | Clinical significance |
|-----------|-----------|----------------------|
| **mrT / mrN** | MRI-estimated T and N stage | Pre-treatment staging; guides neoadjuvant decision |
| **CRM (Circumferential Resection Margin)** | Distance from tumour to mesorectal fascia (surgical edge) | **Clear** >1 mm; **threatened** ≤1 mm; **involved** = 0 mm. Threatened/involved CRM → must have radiotherapy to shrink tumour away from margin |
| **EMVI (Extramural Vascular Invasion)** | Tumour visible inside blood vessels outside the bowel wall | Positive EMVI predicts liver metastases; high-risk feature |
| **ISP (Intersphincteric Plane)** | Space between internal and external anal sphincters | ISP involvement → sphincter-sparing surgery may not be possible |
| **PSW (Posterior Surgical Wall / Presacral Space)** | Plane behind rectum, in front of sacrum | Involvement = advanced disease; complicates dissection |
| **mrTRG (MRI Tumour Regression Grade)** | 1–5 scale assessing treatment response on restaging MRI | mrTRG 1 = complete fibrotic response; mrTRG 5 = no response. Key for Watch and Wait decisions |
| **Tumour height** | Distance from anal verge | Low <5 cm; mid 5–10 cm; upper >10 cm. Low tumours → more complex surgery, higher risk of permanent stoma |

---

## Section 4: Imaging Modalities

### CT (Computed Tomography)

**CT TAP (Thorax, Abdomen, Pelvis)** — standard staging scan for all new colorectal cancers. Reports liver and lung metastases, lymphadenopathy, and complications.

Common CT findings:
- Liver metastases appear as darker (hypodense) areas
- Lung metastases appear as small round nodules
- "**Incidental findings**" (incidentalomas) — unrelated findings (e.g., kidney cysts, aortic aneurysm) that must be documented and followed up

Other CT types: `CT abdomen`, `CT abdomen/pelvis`, `CT colonography`, `CT TAP`.

### MRI (Magnetic Resonance Imaging)

Preferred for **rectal cancer** staging because it shows the layers of the rectal wall, CRM, EMVI, and ISP in detail that CT cannot.

Key MRI sequences:
- **T2-weighted** — fat appears white, tumour appears grey; used for staging
- **DWI (Diffusion-Weighted Imaging)** — detects restricted water movement in dense tumour tissue; used to find residual tumour after treatment

**Restaging MRI** is performed at 6, 8, 10, or 12 weeks after radiotherapy to assess response. A good response shows the tumour replaced by dark **low-signal fibrosis** (scar tissue).

### PET-CT (Positron Emission Tomography-CT)

Functional scan. Patient receives radioactive glucose (**FDG**), which cancer cells consume rapidly. **FDG-avid** = lights up on scan = metabolically active tissue.

Used when CT shows a suspicious lesion but cannot confirm if it is cancer, and before liver surgery for metastases (to check for hidden spread elsewhere).

### ERUS (Endorectal Ultrasound)

Ultrasound probe placed in the rectum. Highly accurate for very early (T1) rectal tumours. Less used now that MRI quality has improved.

---

## Section 5: The MDT Process

### What the MDT Is

The **Multidisciplinary Team (MDT)** is a weekly meeting where every new cancer case is discussed and a treatment plan is agreed. It is not optional — all colorectal cancer patients must go through it.

Attendees:
- **Colorectal surgeon** — can the tumour be removed, and how?
- **Oncologist** — chemotherapy and/or radiotherapy options
- **Radiologist** — presents CT and MRI scans
- **Pathologist** — explains biopsy results
- **Gastroenterologist** — endoscopy findings
- **CNS (Clinical Nurse Specialist)** — knows the patient's wishes, fitness, and social context
- **MDT coordinator** — records the outcome; manages the proforma

### The MDT Proforma

The proforma is the structured data form for each patient. For data scientists: **it is your schema**. Fields typically include:

| Category | Fields |
|----------|--------|
| Demographics | NHS number, hospital number (MRN), name/initials, DOB, gender |
| Cancer targets | 62-day target date, DTT date |
| Diagnosis | ICD-10 code, differentiation, staging, Dukes |
| Endoscopy | Type, date, findings |
| Histology | Biopsy result, biopsy date, MMR status |
| Imaging (CT) | Date, T/N/M/EMVI staging, incidental findings |
| Imaging (MRI) | Date, mrT/mrN/mrEMVI/mrCRM/mrPSW |
| MDT | Meeting date, treatment approach, decision |
| Follow-up | 6-week MRI, flexi sig results, subsequent decisions |

### Time Targets

| Target | Definition |
|--------|-----------|
| **TWR / 2WW** | Urgent GP referral; specialist appointment within 14 days |
| **DTT (Decision to Treat)** | Date MDT-agreed plan is formally accepted by patient; starts 31-day clock |
| **62-day target** | GP urgent referral to first treatment; NHS cancer standard |

### MDT Outcomes You Will See in the Data

- `Refer for surgical review` — patient needs a face-to-face with a surgeon before a decision
- `Long-course CRT then reassess` — neoadjuvant rectal cancer strategy
- `Straight to surgery` — no neoadjuvant treatment needed
- `Plan neoadjuvant CRT and repeat MRI in 6 weeks` — rectal cancer, threatened CRM
- `Rediscuss at MDT` — waiting for more information (e.g., liver MRI result)
- `Watch and Wait` — complete response after radiotherapy; no surgery unless regrowth
- `For colonoscopy / MRI / CT` — further investigation before decision

---

## Section 6: Treatment Pathways

### Surgery

#### Colon Surgery

| Operation | What is removed |
|-----------|----------------|
| **Right hemicolectomy** | Caecum + ascending colon (right-sided tumours) |
| **Left hemicolectomy** | Descending colon |
| **Sigmoid colectomy** | Sigmoid colon |
| **Hartmann's procedure** | Sigmoid/rectum removed + permanent colostomy; no anastomosis (usually emergency) |
| **Subtotal / total colectomy** | Most or all of the colon (multiple polyps, emergency obstruction) |

**CME (Complete Mesocolic Excision)** — the oncological gold standard for colon surgery; analogous to TME for the rectum; removes the tumour within intact mesocolic planes with a high vascular tie.

#### Rectal Surgery

| Operation | What is removed | Outcome |
|-----------|----------------|---------|
| **Anterior resection (AR)** | Rectum and anastomosis to colon | Preserves continence |
| **Low anterior resection (LAR)** | Low rectum with TME | Sphincter-sparing; often needs a temporary ileostomy |
| **APER / APE** | Rectum + anus + sphincters | Permanent colostomy |
| **ELAPE** | As above + levator ani muscles | More radical; for very low tumours; reduces margin positivity |
| **TME (Total Mesorectal Excision)** | Rectum within its intact mesorectal envelope | Gold standard technique; dramatically reduces local recurrence |
| **TEM / TAMIS** | Local excision of early (T1) rectal tumours | No stoma; only for suitable early cancers |
| **Papillon** | Contact radiotherapy; not surgery per se | Alternative to local excision for early cancers in frail patients |

**Defunctioning (temporary) stoma:** A loop ileostomy to divert faeces while an anastomosis heals. Reversed after 3–6 months.

**R0 / R1 / R2 resection:** R0 = clear margins (curative intent); R1 = microscopic margin involvement; R2 = macroscopic tumour left behind.

### Radiotherapy

| Modality | Details | When used |
|----------|---------|-----------|
| **Long-course CRT (nCRT)** | 45–50 Gy in 25–28 fractions over 5–6 weeks, with concurrent capecitabine | Locally advanced rectal cancer with threatened CRM; to shrink tumour before surgery |
| **Short-course RT (SCRT)** | 25 Gy in 5 fractions over 1 week | Resectable rectal cancer; surgery follows after a delay |
| **EBRT (External Beam Radiotherapy)** | Standard delivery method for both above | — |
| **Papillon** | Contact radiotherapy (low-energy X-rays applied directly to tumour) | Early rectal cancer; alternative to surgery in frail patients |

**Watch and Wait (W&W):** If a rectal cancer completely disappears after radiotherapy (confirmed by MRI + endoscopy + examination = **cCR**, complete clinical response), surgery can be avoided. The patient enters intensive surveillance instead. Regrowth occurs in ~25–35% — salvage surgery is then offered.

### Chemotherapy

#### Key Regimens

| Regimen | Components | Context |
|---------|-----------|---------|
| **FOLFOX** | 5-FU + Leucovorin + Oxaliplatin (IV, 2-weekly) | Adjuvant Stage III colon; metastatic CRC first-line |
| **CAPOX / XELOX** | Capecitabine (oral) + Oxaliplatin (3-weekly) | Alternative to FOLFOX; oral option preferred by some patients |
| **FOLFIRI** | 5-FU + Leucovorin + Irinotecan (IV, 2-weekly) | Metastatic CRC; second-line after FOLFOX, or interchangeably first-line |
| **Capecitabine (Xeloda)** | Oral 5-FU prodrug | Concurrent with long-course CRT; adjuvant single agent |

**FOXTROT:** A landmark UK clinical trial (Lancet Oncology 2020) showing that 6 weeks of neoadjuvant FOLFOX chemotherapy before surgery for locally advanced colon cancer reduces incomplete resections and recurrence. In MDT notes, **"FOXTROT"** is shorthand for this neoadjuvant colon cancer approach.

**Neoadjuvant vs adjuvant:**
- **Neoadjuvant** = before surgery; goal is to shrink the tumour ("downstage" it)
- **Adjuvant** = after surgery; goal is to eliminate residual microscopic disease

**TNT (Total Neoadjuvant Therapy):** All chemotherapy and radiotherapy given before surgery, rather than some after. Used for high-risk locally advanced rectal cancer to maximise chance of cure and organ preservation. Investigated in RAPIDO and PRODIGE 23 trials.

### Targeted Therapy and Immunotherapy

| Agent | Target | When eligible |
|-------|--------|--------------|
| **Cetuximab / Panitumumab** | Anti-EGFR | RAS wild-type (both KRAS and NRAS unmutated) AND BRAF wild-type, metastatic CRC, left-sided primary |
| **Bevacizumab (Avastin)** | Anti-VEGF | Added to FOLFOX or FOLFIRI regardless of RAS status; metastatic CRC |
| **Pembrolizumab (Keytruda)** | Anti-PD-1 immunotherapy | MSI-H / dMMR metastatic CRC; now first-line standard (KEYNOTE-177 trial) |
| **Nivolumab (Opdivo)** | Anti-PD-1 immunotherapy | MSI-H / dMMR; used with ipilimumab |

**Critical rule:** Anti-EGFR agents (cetuximab, panitumumab) are **only** effective in RAS/BRAF wild-type, **left-sided** primary metastatic CRC. RAS-mutated tumours are resistant — this is one of the most important biomarker-treatment interactions in the whole of oncology.

### Local Treatments for Metastatic Disease

| Treatment | What it is | When used |
|-----------|-----------|-----------|
| **Liver resection** | Surgical removal of liver metastases (CRLM) | Potentially curative; ~40–50% 5-year survival in selected patients |
| **SIRT / Radioembolisation** | Y-90 microspheres injected into hepatic artery | Liver-dominant unresectable disease |
| **SABR** | Stereotactic ablative radiotherapy; ultra-precise high-dose beams | Oligometastatic disease (1–5 discrete metastases); liver, lung, local recurrence |
| **RFA / Microwave ablation** | Heat destroys small liver tumours (<3 cm) | Liver metastases not suitable for surgery |
| **HIPEC** | Hyperthermic intraperitoneal chemotherapy; given at surgery | Peritoneal metastases (CRS + HIPEC) in selected patients |

---

## Section 7: Pathway Walkthrough Summaries

### 1. Early Colon Cancer (T1/T2 N0 M0) — Straight to Surgery

A patient with iron-deficiency anaemia is referred via the 2WW pathway. Colonoscopy finds a 2 cm cancer in the ascending colon (biopsied and **tattooed**). CT TAP: no metastases.
→ MDT decision: right hemicolectomy (no neoadjuvant treatment needed).
→ Surgery within 31 days of DTT. Pathology confirms pT2N0M0, R0 resection.
→ MDT rediscussion: Stage I, no adjuvant chemotherapy. Surveillance (CT year 1 and 3; colonoscopy year 1).

### 2. Locally Advanced Rectal Cancer (T3 Threatened CRM) — Neoadjuvant CRT

A patient presents with rectal bleeding. MRI shows mrT3c low rectal cancer (5 cm from anal verge), mrCRM 0.5 mm (threatened), mrEMVI positive.
→ MDT decision: long-course CRT (45 Gy / 25 fractions + concurrent capecitabine).
→ Restaging MRI at 8 weeks: mrTRG 2 (near-complete response), CRM now clear.
→ MDT rediscussion: proceed to low anterior resection + TME. Pathological stage ypT1N0M0.
→ Surveillance: CT years 1 and 3; MRI pelvis year 1; colonoscopy year 1; 6-monthly CEA.

### 3. Metastatic Colorectal Cancer (M1) — Systemic Chemotherapy

Sigmoid cancer with multiple liver metastases + lung nodules on CT. MMR: pMMR. KRAS mutated.
→ MDT decision: palliative FOLFOX + bevacizumab (KRAS mutated → no anti-EGFR; pMMR → no immunotherapy as monotherapy).
→ After 8 cycles: CT shows liver metastases smaller and now technically resectable.
→ Hepatobiliary MDT: two-stage hepatectomy planned. Lung nodule resected.
→ Post-resection: adjuvant CAPOX. CEA normalises.

### 4. Rectal Cancer — Watch and Wait After Complete Clinical Response

Low rectal cancer (mrT3b, 4 cm from anal verge, threatened CRM). After long-course CRT: MRI shows mrTRG 1 (complete fibrotic response), CRM clear. Sigmoidoscopy shows pale scar, no tumour.
→ MDT decision: cCR established → Watch and Wait (patient wishes to avoid permanent stoma).
→ Surveillance: MRI + rigid sigmoidoscopy + DRE + CEA every 3 months for 2 years, then 6-monthly.
→ At 24 months: small mucosal regrowth found on endoscopy. MRI confirms confined recurrence.
→ Salvage ELAPE (permanent colostomy). Pathology: ypT2N0.

---

## Section 8: Glossary of Acronyms and Abbreviations

Alphabetically sorted. All terms relevant to colorectal cancer MDT documentation.

| Term | Expansion | Definition |
|------|-----------|------------|
| **2WW / TWR** | Two-Week Wait / Two-Week Rule | NHS urgent GP cancer referral; specialist appointment within 14 days. |
| **5-FU** | 5-Fluorouracil | Core chemotherapy agent; inhibits DNA synthesis; component of FOLFOX, FOLFIRI, CRT. |
| **62-day target** | 62-day treatment target | NHS standard: treatment must start within 62 days of urgent GP referral. |
| **AAA** | Abdominal Aortic Aneurysm | Common incidental finding on staging CT. |
| **AJCC** | American Joint Committee on Cancer | US body co-maintaining TNM staging with UICC. |
| **APE / APER** | Abdominoperineal Excision of Rectum | Surgery removing rectum, anus, and sphincters; permanent colostomy. |
| **AR** | Anterior Resection | Rectum removed with colon rejoined; sphincter-preserving. |
| **BCSP** | Bowel Cancer Screening Programme | NHS biennial FIT testing for ages 50–74. |
| **bevacizumab** | — (brand: Avastin) | Anti-VEGF monoclonal antibody; anti-angiogenic; used in metastatic CRC. |
| **BRAF** | B-Raf Proto-Oncogene | Mutated in ~10% of mCRC (V600E mutation); poor prognosis; targetable. |
| **BSC** | Best Supportive Care | Symptom management only; no tumour-directed therapy. |
| **CAPOX / XELOX** | Capecitabine + Oxaliplatin | Oral/IV chemotherapy regimen; 3-weekly; adjuvant and metastatic CRC. |
| **cCR** | Complete Clinical Response | No detectable tumour by imaging, endoscopy, or examination after treatment; criterion for Watch and Wait. |
| **CEA** | Carcinoembryonic Antigen | Blood tumour marker; used for monitoring response and surveillance; elevated in ~70% of advanced CRC. |
| **cetuximab** | — (brand: Erbitux) | Anti-EGFR monoclonal antibody; RAS/BRAF wild-type metastatic CRC only. |
| **CIMP** | CpG Island Methylator Phenotype | Epigenetic silencing of tumour suppressor genes; associated with serrated pathway and MSI-H. |
| **CME** | Complete Mesocolic Excision | Oncological colon surgery technique analogous to TME; removes tumour within intact mesocolic planes. |
| **CNS** | Clinical Nurse Specialist | Specialist nurse; key worker for colorectal cancer patients; attends MDT. |
| **CR / cCR / pCR** | Complete Response (clinical / pathological) | No residual tumour after treatment; clinical = by imaging; pathological = by specimen examination. |
| **CRC** | Colorectal Cancer | — |
| **CRM** | Circumferential Resection Margin | Distance between tumour and mesorectal fascia; clear >1 mm; threatened ≤1 mm; involved = 0 mm. |
| **CRLM** | Colorectal Liver Metastases | Liver spread from CRC; potentially resectable in selected patients. |
| **CRS** | Cytoreductive Surgery | Surgery to remove all visible peritoneal tumour; typically combined with HIPEC. |
| **CRT** | Chemoradiotherapy | Combined chemotherapy (capecitabine) + EBRT; neoadjuvant treatment for rectal cancer. |
| **CT** | Computed Tomography | Cross-sectional X-ray; CT TAP = standard staging scan. |
| **CTC** | CT Colonography (Virtual Colonoscopy) | CT imaging of the insufflated colon; alternative to colonoscopy when incomplete or contraindicated. |
| **DCE** | Dynamic Contrast Enhancement | MRI sequence assessing tissue perfusion; used in advanced imaging protocols. |
| **dMMR** | Deficient Mismatch Repair | Loss of one or more MMR proteins; associated with MSI-H; predicts immunotherapy sensitivity. |
| **DRE** | Digital Rectal Examination | Clinical examination of rectum by gloved finger; assesses tumour fixity and distance from anal verge. |
| **DTT** | Decision to Treat | Formal date MDT plan is accepted; starts 31-day treatment clock. |
| **DWI** | Diffusion-Weighted Imaging | MRI sequence detecting dense tumour tissue; used to assess residual tumour after treatment. |
| **EBRT** | External Beam Radiotherapy | Radiotherapy from external machine; encompasses long-course CRT and SCRT. |
| **EGFR** | Epidermal Growth Factor Receptor | Cell surface receptor; overexpressed in ~80% of CRC; targeted by cetuximab and panitumumab. |
| **ELAPE** | Extralevator Abdominoperineal Excision | Extended APE removing levator ani muscles; wider margin for very low rectal tumours. |
| **EMVI** | Extramural Vascular Invasion | Tumour in blood vessels outside bowel wall; positive = higher metastatic risk; detected by MRI (mrEMVI) or pathology (pEMVI). |
| **ERUS** | Endorectal Ultrasound | Intraluminal ultrasound probe; best for staging early T1/T2 rectal tumours. |
| **FAP** | Familial Adenomatous Polyposis | Hereditary APC gene mutation; hundreds of adenomas; near-certain CRC without prophylactic surgery. |
| **FBC** | Full Blood Count | Routine blood test; anaemia common in right-sided CRC. |
| **FDG** | Fluorodeoxyglucose (18F-FDG) | Radioactive glucose tracer for PET-CT; FDG-avid = metabolically active tumour. |
| **FIT** | Faecal Immunochemical Test | Quantitative stool test detecting human haemoglobin; used in BCSP; positive → colonoscopy referral. |
| **Flexi sig** | Flexible Sigmoidoscopy | Endoscopy of rectum and sigmoid (~60 cm from anus). |
| **FLR** | Future Liver Remnant | Volume of liver remaining after hepatic resection; must be ≥20–30% of total to avoid liver failure. |
| **FOLFIRI** | Folinic acid + 5-FU + Irinotecan | IV chemotherapy; first- or second-line metastatic CRC. |
| **FOLFOX** | Folinic acid + 5-FU + Oxaliplatin | Standard IV chemotherapy; adjuvant Stage III and metastatic CRC. |
| **FOXTROT** | Fluoropyrimidine, Oxaliplatin and Targeted Receptor pre-Operative Therapy | UK trial (Lancet Oncology 2020) establishing neoadjuvant FOLFOX for locally advanced colon cancer. |
| **HER2** | Human Epidermal Growth Factor Receptor 2 | Amplified in ~2–3% of mCRC; emerging targetable biomarker; confers resistance to anti-EGFR. |
| **HIPEC** | Hyperthermic Intraperitoneal Chemotherapy | Heated chemotherapy into peritoneal cavity at surgery; used for peritoneal metastases (CRS + HIPEC). |
| **HNPCC** | Hereditary Non-Polyposis Colorectal Cancer | Historical term for Lynch syndrome. |
| **ICD-10** | International Classification of Diseases, 10th Revision | WHO coding; colorectal cancers C18–C20. |
| **ICV** | Ileocaecal Valve | Junction between small and large bowel; reaching it confirms complete colonoscopy. |
| **IHC** | Immunohistochemistry | Lab staining of tissue for proteins (MMR, HER2, etc.); detects dMMR. |
| **IMRT** | Intensity Modulated Radiotherapy | Advanced EBRT technique; minimises dose to organs at risk. |
| **ISP** | Intersphincteric Plane | Space between internal and external anal sphincters; involvement affects sphincter-preserving surgery. |
| **KRAS** | Kirsten Rat Sarcoma Viral Proto-Oncogene | Most commonly mutated gene in CRC (~40–45%); mutated = resistant to anti-EGFR agents. |
| **LAR** | Low Anterior Resection | Sphincter-sparing surgery for low/mid rectal cancer with TME; usually requires temporary ileostomy. |
| **Lynch syndrome** | — | Hereditary dMMR (germline MMR gene mutation); associated with MSI-H CRC at young age; requires genetic counselling. |
| **MDT** | Multidisciplinary Team | Weekly expert meeting to agree treatment plan for every cancer patient. |
| **MMR** | Mismatch Repair | DNA repair system; key proteins MLH1, MSH2, MSH6, PMS2; deficiency = dMMR = MSI-H. |
| **MRI** | Magnetic Resonance Imaging | Primary staging tool for rectal cancer; superior soft tissue contrast. |
| **mrCRM** | MRI-reported Circumferential Resection Margin | Distance from tumour to mesorectal fascia on MRI. |
| **mrEMVI** | MRI-detected Extramural Vascular Invasion | EMVI identified on MRI as tumour signal in a perirectal vessel. |
| **mrN** | MRI-determined Nodal Stage | Lymph node status on MRI; less accurate than pathological staging. |
| **mrT** | MRI-determined T Stage | Depth of bowel wall invasion on high-resolution MRI. |
| **mrTRG** | MRI Tumour Regression Grade | 5-point scale assessing response on restaging MRI; mrTRG 1 = complete fibrosis, mrTRG 5 = no response. |
| **MSI** | Microsatellite Instability | Genomic instability from dMMR; MSI-H = high instability. |
| **MSI-H** | Microsatellite Instability — High | Functional consequence of dMMR; immunotherapy-sensitive. |
| **MSS** | Microsatellite Stable | Equivalent to pMMR; ~85% of CRC; standard chemotherapy applies. |
| **N stage** | Nodal Stage (TNM) | N0 (none) → N2b (≥7 nodes). |
| **nCRT** | Neoadjuvant Chemoradiotherapy | CRT given before surgery; synonymous with preoperative CRT for rectal cancer. |
| **NRAS** | Neuroblastoma Rat Sarcoma Viral Proto-Oncogene | Mutated in ~5% of mCRC; also predicts anti-EGFR resistance. |
| **panitumumab** | — (brand: Vectibix) | Fully human anti-EGFR; RAS wild-type mCRC; alternative to cetuximab. |
| **Papillon** | — | Contact radiotherapy; low-energy X-rays applied directly to early rectal tumour; organ-preserving option. |
| **pembrolizumab** | — (brand: Keytruda) | Anti-PD-1 immunotherapy; first-line for MSI-H/dMMR metastatic CRC (KEYNOTE-177). |
| **PET-CT** | Positron Emission Tomography-CT | Functional + structural imaging; FDG-avid lesions = active cancer. |
| **pMMR** | Proficient Mismatch Repair | All MMR proteins present; microsatellite stable. |
| **PR** | Partial Response | Tumour shrinks significantly (≥30% by RECIST) but does not disappear. |
| **PSW** | Posterior Surgical Wall / Presacral Space | Anatomical plane behind mesorectum, in front of sacrum; involvement = advanced disease. |
| **PVE** | Portal Vein Embolisation | Radiological occlusion of portal vein to induce hypertrophy of FLR before major hepatectomy. |
| **R0 / R1 / R2** | Resection Margin Status | R0 = microscopically clear (curative); R1 = microscopic involvement; R2 = macroscopic residual tumour. |
| **RAS** | Rat Sarcoma Viral Oncogene Family (KRAS + NRAS) | "RAS wild-type" = both KRAS and NRAS unmutated; required for anti-EGFR eligibility. |
| **RECIST** | Response Evaluation Criteria in Solid Tumours | Standard imaging criteria for measuring tumour response; ≥30% shrinkage = partial response. |
| **RFA** | Radiofrequency Ablation | Heat-based destruction of liver or lung metastases; best for lesions <3 cm. |
| **SABR / SBRT** | Stereotactic Ablative Radiotherapy / Stereotactic Body Radiation Therapy | Ultra-precise high-dose radiotherapy; oligometastatic disease or local recurrence. |
| **SCRT** | Short-Course Radiotherapy | 25 Gy in 5 fractions over 1 week; preoperative rectal cancer. |
| **SIRT** | Selective Internal Radiation Therapy (Radioembolisation) | Y-90 microspheres into hepatic artery; local radiotherapy for liver-dominant metastatic CRC. |
| **SM1 / SM2 / SM3** | Submucosal invasion depth (thirds) | Subdivision of T1 tumours; SM3 = deep invasion → usually requires radical surgery. |
| **SSL** | Sessile Serrated Lesion | Flat polyp; difficult to detect; associated with BRAF mutation and MSI-H tumours. |
| **T stage** | Tumour Stage (TNM) | Tis → T4b; depth of primary tumour invasion. |
| **TAMIS** | Transanal Minimally Invasive Surgery | Local excision of early rectal tumours using laparoscopic instruments via transanal port. |
| **tattoo / endoscopic tattoo** | — | Ink injected submucosally at endoscopy to mark tumour site for surgical identification. |
| **TEM** | Transanal Endoscopic Microsurgery | Rigid rectoscope technique for local excision of early rectal tumours (T1 sm1–sm2). |
| **TME** | Total Mesorectal Excision | Gold-standard rectal surgery; removes rectum within intact mesorectal envelope; dramatically reduces local recurrence. |
| **TNM** | Tumour, Node, Metastasis | Universal cancer staging system (8th edition, UICC/AJCC). |
| **TNT** | Total Neoadjuvant Therapy | All chemotherapy and radiotherapy given before surgery; high-risk locally advanced rectal cancer. |
| **TRG** | Tumour Regression Grade | Pathological scale assessing tumour cell kill and fibrosis after neoadjuvant treatment. |
| **TWR** | Two-Week Rule | Synonymous with 2WW; urgent GP referral pathway. |
| **UICC** | Union for International Cancer Control | International body co-maintaining TNM with AJCC. |
| **VEGF** | Vascular Endothelial Growth Factor | Protein promoting tumour angiogenesis; targeted by bevacizumab. |
| **W&W** | Watch and Wait | Active surveillance for cCR after neoadjuvant treatment; surgery avoided unless regrowth. |
| **Y-90** | Yttrium-90 | Radioactive isotope loaded into SIRT microspheres. |
| **ypT / ypN** | Post-neoadjuvant pathological TNM | Staging of resection specimen after neoadjuvant treatment; ypT0N0 = pathological complete response (pCR). |

---

## Key Sources

- NICE NG151 (2020): Colorectal Cancer
- NICE NG12 (2015, updated 2023): Suspected Cancer Referral
- ACPGBI Guidelines: Management of Cancer of the Colon, Rectum and Anus (2017)
- ESMO Clinical Practice Guidelines: Metastatic Colorectal Cancer (2023); Rectal Cancer (2017)
- BSG / ACPGBI Colorectal Cancer Pathway Guidance (2022)
- TNM Classification of Malignant Tumours, 8th Edition (UICC/AJCC, 2017)
- FOXTROT trial: Lancet Oncology 2020
- RAPIDO trial: Lancet Oncology 2021
- PRODIGE 23 trial: Lancet Oncology 2021
- KEYNOTE-177: NEJM 2020
- MERCURY Study Group (CRM/MRI): Radiology 2007
- International Watch and Wait Database (IWWD): Lancet 2018
- NHS Bowel Cancer Screening Programme Operational Guidance (2020)

---

*Consolidated from three deep-research reports (Grok, Gemini, Claude.ai) by Claude Code, March 2026.*
