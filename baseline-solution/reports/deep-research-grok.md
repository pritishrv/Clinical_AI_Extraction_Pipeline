# Research Report: Colorectal Cancer for Non-Clinicians in Clinical AI Hackathons

## Section 1: What Is Colorectal Cancer?

**Colorectal cancer** (also known as bowel cancer) is a malignant tumor arising from the inner lining of the large intestine, which includes the colon and rectum. It is one of the most common cancers worldwide and develops from abnormal growths called polyps that can become cancerous over time.

- **Anatomy**: The colon and rectum form the final part of the digestive tract. The colon is divided into segments: the **caecum** (where the small intestine connects), **ascending colon** (right side, rising upward), **transverse colon** (across the abdomen), **descending colon** (left side, downward), and **sigmoid colon** (S-shaped, connecting to the rectum). The **rectum** is the last 12-15 cm leading to the anus. Clinical significance of location includes: right-sided tumors (caecum, ascending, proximal transverse) often present later with anemia or vague symptoms due to wider lumen; left-sided (descending, sigmoid) cause obstruction or bleeding earlier; rectal tumors may involve sphincter muscles, affecting continence and requiring specific surgical considerations like preserving anal function.

- **How colorectal cancer develops**: Most cases follow the **adenoma-carcinoma sequence**, where benign polyps (adenomas) accumulate genetic mutations over 10-15 years and transform into cancer. Polyp types include **adenomatous polyps** (precancerous, tubular, villous, or tubulovillous), **serrated polyps** (hyperplastic or sessile serrated, some with malignant potential), and **inflammatory polyps** (non-precancerous). Risk increases with mutations in genes like APC, KRAS, or TP53.

- **Epidemiology**: In 2026, an estimated 158,850 new cases of colorectal cancer are projected in the US, with 55,230 deaths. Worldwide, there were about 1.9 million new cases and over 900,000 deaths in 2022. Incidence is highest in high-income countries like Europe, Australia, and New Zealand, but declining in older adults (≥65) by 2.5% annually due to screening, while rising sharply in younger adults (20-49) by 3% annually and in 50-64 by 0.4%, driven by distal colon and rectal tumors. Risk factors include age (>50), family history, obesity, sedentary lifestyle, diets high in processed/red meats and low in fiber/fruits/vegetables, smoking, alcohol, inflammatory bowel disease (IBD), and diabetes. Screening rationale: Early detection via programs like fecal immunochemical test (FIT) or colonoscopy reduces mortality by 16-30% by removing precancerous polyps or catching early-stage disease.

- **Histological subtypes**: The vast majority (95%) are **adenocarcinomas** (gland-forming). Variants include **mucinous adenocarcinoma** (mucus-producing, >50% mucin, poorer prognosis), **signet ring cell carcinoma** (cells with intracellular mucin, aggressive), and rare types like squamous cell, adenosquamous, or neuroendocrine tumors.

- **Differentiation grades**: Describes how closely cancer cells resemble normal cells. **Well-differentiated** (low-grade, organized glands); **moderately differentiated** (intermediate); **poorly differentiated** (high-grade, disorganized, aggressive with worse prognosis).

- **ICD-10 codes relevant to colorectal cancer**: 
  - **C18**: Malignant neoplasm of colon (subcodes: C18.0 caecum, C18.1 appendix, C18.2 ascending, C18.3 hepatic flexure, C18.4 transverse, C18.5 splenic flexure, C18.6 descending, C18.7 sigmoid, C18.8 overlapping, C18.9 unspecified).
  - **C19**: Malignant neoplasm of rectosigmoid junction.
  - **C20**: Malignant neoplasm of rectum.
  - Related: C21 for anus/anal canal; D01.0-2 for carcinoma in situ.

## Section 2: Detection and Investigation

Colorectal cancer is often detected through screening or investigation of symptoms. Early detection improves outcomes, with pathways emphasizing rapid assessment.

- **Symptoms that trigger investigation and the TWR / DTT / 2WW pathway**: Common symptoms include rectal bleeding, change in bowel habits (diarrhea/constipation), abdominal pain, weight loss, anemia, or obstruction. The **Two-Week Rule (TWR)** or **Two-Week Wait (2WW)** is a UK NHS pathway for urgent referral of suspected cancer, aiming for specialist assessment within 14 days. **Decision to Treat (DTT)** marks the point when a treatment plan is agreed, starting the clock for targets like 62-day treatment initiation.

- **Endoscopy types used**:
  - **Colonoscopy**: Full examination of the colon and rectum using a flexible tube with camera. **Complete** if it reaches the **ileocaecal valve (ICV)** (junction of small and large intestine), confirming full visualization; **incomplete** if not, often requiring follow-up imaging.
  - **Flexible sigmoidoscopy (flexi sig)**: Examines rectum and sigmoid/left colon; quicker, less sedation.
  - **Rigid sigmoidoscopy**: Short, rigid tube for rectum/low sigmoid; used in clinics.
  - **CT colonography (virtual colonoscopy)**: CT scan with air insufflation for 3D colon images; alternative for incomplete colonoscopy or frail patients.
  - **Tattoo** in endoscopy report: Injection of ink to mark polyp/tumor site for easy identification during surgery.
  - **ICV**: Ileocaecal valve; reaching it confirms complete colonoscopy, ensuring no right-sided lesions are missed.

- **Biopsy and histopathology**:
  - **Biopsy report contents**: Specimen type, tumor location, histological subtype (e.g., adenocarcinoma), invasion depth, margins, lymphovascular invasion, and molecular markers.
  - **Differentiation grade**: As above (well/moderate/poor).
  - **MMR (Mismatch Repair) status**: Proteins (MLH1, MSH2, MSH6, PMS2) repair DNA errors. **MMR deficient (dMMR)** indicates instability, linked to Lynch syndrome (hereditary) or sporadic; eligible for immunotherapy. **MMR proficient (pMMR)** is stable.
  - **MSI (Microsatellite Instability)**: Related to MMR; **MSI-high (MSI-H)** correlates with dMMR, better prognosis, immunotherapy response.
  - **IHC (Immunohistochemistry)**: Staining for proteins like MMR or HER2 to guide therapy.
  - **KRAS, NRAS, BRAF mutation testing**: In RAS/RAF pathway; **RAS wild-type** allows anti-EGFR therapy (cetuximab); BRAF V600E (5-10%) indicates poor prognosis, targeted options.

- **Blood tests**:
  - **CEA (Carcinoembryonic Antigen)**: Tumor marker produced by some cancers. Normal range <5 ng/mL (non-smokers), <10 ng/mL (smokers). Used for monitoring recurrence/response, not screening (low sensitivity/specificity); elevated in 70% advanced cases but also benign conditions like smoking or IBD.

## Section 3: Staging

Staging determines cancer extent, guiding treatment. The primary system is **TNM** (AJCC 8th edition, effective 2018; no major changes in 9th for colorectal).

- **TNM staging system in detail**:
  - **T stage** (primary tumor): T0 (no tumor), Tis (carcinoma in situ, intraepithelial/intramucosal), T1 (submucosa invasion), T2 (muscularis propria), T3 (through muscularis into pericolic tissue), T4a (peritoneal penetration), T4b (adjacent organs). For early polyps: sm1/sm2/sm3 (submucosal invasion thirds, risk of lymph node mets increases with depth).
  - **N stage** (nodes): N0 (none), N1a (1 node), N1b (2-3), N1c (tumor deposits without nodes), N2a (4-6), N2b (≥7).
  - **M stage** (metastasis): M0 (none), M1a (one organ), M1b (multiple organs), M1c (peritoneum ± others).
  - **Prefixes**: **c** (clinical, pre-treatment imaging/symptoms), **p** (pathological, post-resection), **mr** (MRI-based for rectal), **y** (post-neoadjuvant), **r** (recurrent).

- **Dukes staging**: Historical (1932), still referenced: A (T1-2 N0 M0, confined to wall), B (T3-4 N0 M0, through wall), C (N+ any T M0), D (M1). Replaced by TNM for detail but appears in older literature.

- **Integrated TNM stage groupings**: Stage 0 (Tis N0 M0), I (T1-2 N0 M0), IIA (T3 N0 M0), IIB (T4a N0 M0), IIC (T4b N0 M0), IIIA (T1-2 N1/N1c M0 or T1 N2a M0), IIIB (T3-4a N1/N1c M0 or T2-3 N2a M0 or T1-2 N2b M0), IIIC (T4a N2a M0 or T3-4a N2b M0 or T4b N1-2 M0), IVA (any T any N M1a), IVB (M1b), IVC (M1c).

- **Specific MRI staging parameters for rectal cancer**:
  - **mrT, mrN**: MRI-estimated T/N, more precise for local extent than clinical.
  - **CRM (Circumferential Resection Margin)**: Distance to mesorectal fascia; **clear (>1mm)**, **threatened (≤1mm)**, or **involved (0mm)**; threatened/involved increases recurrence risk, prompts neoadjuvant therapy.
  - **EMVI (Extramural Vascular Invasion)**: Tumor in veins outside bowel wall; positive indicates higher metastasis risk.
  - **ISP (Intersphincteric Plane)**: Space between sphincters; involvement affects sphincter-sparing surgery feasibility.
  - **PSW (Posterior Surgical Wall / Presacral Space)**: Area behind rectum; tumor extension here complicates resection.
  - **Low / mid / upper rectal tumour**: Measured from anal verge (low <5cm, mid 5-10cm, upper >10cm); low tumors often need neoadjuvant therapy, risk fecal incontinence.

- **Difference between colon cancer staging and rectal cancer staging**: Colon relies more on CT for distant mets; rectal emphasizes MRI for local details (CRM, EMVI) due to surgical challenges in pelvis and higher local recurrence risk.

## Section 4: Imaging Modalities

Imaging confirms diagnosis, stages disease, and monitors response.

- **CT (Computed Tomography)**:
  - **CT TAP (Thorax, Abdomen, Pelvis)**: Standard for staging, assesses local invasion, nodes, mets.
  - **CT abdomen/pelvis**: Focused on primary/metastatic sites.
  - **CT colonography**: For detection if endoscopy incomplete.
  - **CT staging report expectations**: Tumor location/size, T/N/M stages, vascular involvement, mets (e.g., liver segments), complications like perforation.
  - **Incidental findings**: Unrelated issues (e.g., other tumors, aneurysms) requiring follow-up.
  - **Metastatic patterns**: Liver (most common), lungs, peritoneum (carcinomatosis), distant nodes.

- **MRI (Magnetic Resonance Imaging)**:
  - Preferred for rectal staging due to soft tissue detail.
  - **MRI pelvis / MRI rectum**: Assesses tumor depth, nodes, CRM.
  - **High-resolution rectal MRI protocol**: Thin slices, multiplanar, for precise mrT/mrN/EMVI.
  - **Low signal on MRI**: Indicates fibrosis/scarring (e.g., post-treatment response).
  - **Response assessment MRI**: Post-neoadjuvant; e.g., 6-week (early), 10-week (standard), 12-week (delayed) after CRT to evaluate downstaging/CR.
  
- **PET-CT (Positron Emission Tomography CT)**:
  - **FDG-avid**: Tumor uptake of glucose tracer; highlights active cancer.
  - Used for equivocal mets, recurrence, or pre-metastasectomy.
  - Differs from CT: Adds metabolic info to anatomy; better for small/distant lesions.

- **Ultrasound**:
  - **ERUS (Endorectal Ultrasound)**: Probe in rectum; stages early T1-2 rectal tumors, assesses depth/nodes; less used now vs. MRI.

## Section 5: MDT (Multidisciplinary Team) Process

The **MDT** ensures collaborative decision-making for optimal care.

- **What an MDT is**: Weekly meeting of experts: **colorectal surgeon** (operates), **oncologist** (chemo/radio), **radiologist** (interprets imaging), **pathologist** (analyzes biopsies), **gastroenterologist** (endoscopy), **CNS (Clinical Nurse Specialist)** (patient support), **MDT coordinator** (logistics). Decisions include staging confirmation, treatment plan, surveillance.

- **MDT proforma**: Standardized form for referrals/discussions; fields include patient demographics, NHS number, referrer, clinical details (symptoms, PMH, meds), performance status (ECOG/PS), BMI, comorbidities, diagnosis date, histology, imaging (CT/MRI/PET dates/locations), prior treatment, question for MDT (e.g., resectability), and outcomes (e.g., surgery, chemo).

- **The flow from referral to MDT discussion to treatment decision**: Symptom/referral (e.g., 2WW) → investigations (endoscopy/biopsy/imaging) → MDT review → plan (e.g., surgery) → patient discussion → treatment → follow-up MDT if needed.

- **What "rediscuss at MDT" means**: Case returns due to new info (e.g., post-treatment response, complications, recurrence).

- **MDT outcome categories**: Curative surgery, neoadjuvant therapy, palliative chemo, best supportive care (BSC), further tests, surveillance.

- **Cancer target dates**:
  - **62-day target**: From urgent referral to first treatment; monitors efficiency.
  - **DTT**: Formal decision to proceed with treatment.
  - **TWR / 2WW**: Urgent pathway for suspected cancer.

- **BCSP (Bowel Cancer Screening Programme)**: UK program for ages 56-74 (expanding to 50-74); sends FIT kit every 2 years. Positive FIT (>120 μg/g) → colonoscopy at screening center. If cancer found, referred to MDT for staging/treatment; integrates via data entry to national system.

## Section 6: Treatment Pathways

Treatments aim for cure or palliation, based on stage/location.

#### Surgery
- **Types for colon cancer**:
  - **Right hemicolectomy**: Removes right colon/caecum.
  - **Left hemicolectomy**: Left colon.
  - **Sigmoid colectomy**: Sigmoid.
  - **Anterior resection (AR)**: Rectosigmoid, preserves anus.
  - **Hartmann's procedure**: Resection with colostomy, no anastomosis.
  - **Subtotal / total colectomy**: Extensive disease.
- **Types for rectal cancer**:
  - **Anterior resection (low / ultra-low)**: For mid/upper, with anastomosis.
  - **ELAPE (Extralevator Abdominoperineal Excision)**: Removes rectum/anus/sphincter, permanent colostomy; for low tumors.
  - **APE / APER (Abdominoperineal Excision of Rectum)**: Similar to ELAPE but less extensive.
  - **TME (Total Mesorectal Excision)**: Gold standard; removes mesorectum en bloc to reduce recurrence.
  - **Local excision**: **TEM (Transanal Endoscopic Microsurgery)** or **TAMIS** for early T1; **Papillon** (contact RT) for frail.
  - **Defunctioning stoma**: Temporary loop ileostomy/colostomy to divert feces, protect anastomosis.
- **Surgical review**: MDT referral for operability assessment.
- **Tattooing**: Endoscopic ink mark for laparoscopic identification.

#### Radiotherapy
- **Long-course CRT (Chemoradiotherapy)**: 45-50.4 Gy in 25-28 fractions over 5-6 weeks, with concurrent capecitabine; for locally advanced rectal.
- **Short-course RT (SCRT)**: 25 Gy in 5 fractions; pre-surgery for resectable rectal.
- **EBRT (External Beam Radiotherapy)**: Standard delivery method.
- **Papillon**: Contact X-ray for early rectal; alternative to surgery.
- **Response**: **Complete response (CR)** (no tumor), near-CR, partial (PR).
- **Watch and Wait (W&W)**: No surgery after CR; surveillance with MRI/endoscopy; risks recurrence (20-30%).

#### Chemotherapy
- **FOXTROT trial and regimen**: Phase III trial showed neoadjuvant FOLFOX (6 weeks) for operable colon downstages tumor, reduces incomplete resections/recurrence by 28%; regimen: oxaliplatin + 5-FU/leucovorin.
- **FOLFOX**: 5-FU (fluorouracil, IV), oxaliplatin, leucovorin; adjuvant/neoadjuvant for stage III/ high-risk II.
- **FOLFIRI**: 5-FU, irinotecan, leucovorin; for mets, if oxaliplatin fails.
- **CAPOX / XELOX**: Capecitabine (oral), oxaliplatin; equivalent to FOLFOX, oral convenience.
- **Capecitabine (Xeloda)**: Oral prodrug to 5-FU; in CRT for rectal.
- **Neoadjuvant chemotherapy**: Pre-surgery to shrink/downstage; "downstaging" reduces T/N stage.
- **TNT (Total Neoadjuvant Therapy)**: All chemo/RT pre-surgery for rectal.
- **Adjuvant chemotherapy**: Post-surgery for node-positive/high-risk; 3-6 months.

#### Targeted Therapy and Immunotherapy
- **Anti-EGFR agents (cetuximab, panitumumab)**: For RAS-wild-type mets; blocks growth signaling.
- **Anti-VEGF agents (bevacizumab)**: Inhibits angiogenesis; with chemo for mets.
- **Immunotherapy (pembrolizumab, nivolumab)**: Checkpoint inhibitors for MSI-H/dMMR (10-15%); first-line for advanced.
- Replaces chemo in MSI-H cases with high response rates.

#### Local Treatments for Metastatic Disease
- **Liver resection**: For resectable liver mets; curative potential.
- **SIRT (Selective Internal Radiation Therapy)**: Yttrium-90 beads to liver tumors.
- **SABR (Stereotactic Ablative Radiotherapy)**: High-dose RT for small mets.
- **Ablation**: **RFA (Radiofrequency)** or microwave; destroys tumors via heat.

## Section 7: Pathway Summaries

1. **A patient with early colon cancer (T1/T2, N0, M0)**: Referred via symptoms or screening. Investigations confirm localized tumor. MDT discusses: straight to surgery (e.g., hemicolectomy) for resection and staging. Post-op pathology confirms stage I; no adjuvant therapy needed unless high-risk features. Follow-up with CEA, CT, colonoscopy.

2. **A patient with locally advanced rectal cancer (T3/T4, CRM threatened)**: Urgent referral, MRI shows threatened CRM/EMVI. MDT recommends neoadjuvant long-course CRT to downstage. Restaging MRI at 6-10 weeks assesses response. If good, proceed to surgery (e.g., low AR with TME). Post-op adjuvant chemo if nodes positive. Surveillance for recurrence.

3. **A patient with metastatic colorectal cancer (M1)**: Staging CT/PET shows liver/lung mets. MDT assesses resectability; if unresectable, systemic chemotherapy (e.g., FOLFOX + bevacizumab) or targeted/immuno if biomarkers match. Rediscuss after cycles for response; possible met-directed therapy (resection/SIRT) if downstaged. Palliative focus if progression.

4. **A rectal cancer patient suitable for Watch and Wait after complete clinical response**: Locally advanced rectal; neoadjuvant CRT. Post-treatment MRI/endoscopy/biopsy show CR (no residual tumor). MDT opts for W&W instead of surgery. Intensive surveillance: MRI/endoscopy every 3-6 months initially, then annually; CEA checks. If recurrence, salvage surgery.

## Section 8: Glossary of Acronyms and Abbreviations

- **2WW**: Two-Week Wait; urgent NHS referral pathway for suspected cancer to ensure specialist review within 14 days.
- **5-FU**: 5-Fluorouracil; chemotherapy drug that inhibits DNA synthesis, used in regimens like FOLFOX.
- **APE**: Abdominoperineal Excision; surgery removing rectum and anus, creating permanent colostomy.
- **AR**: Anterior Resection; surgery removing part of rectum/sigmoid with anastomosis to preserve continence.
- **BCSP**: Bowel Cancer Screening Programme; UK national screening using FIT to detect early colorectal cancer.
- **BRAF**: B-Raf proto-oncogene; mutation (e.g., V600E) in 5-10% cases, associated with poor prognosis and targeted therapies.
- **BSC**: Best Supportive Care; palliative management focusing on symptoms without curative intent.
- **CAPOX**: Capecitabine + Oxaliplatin; chemotherapy regimen, often adjuvant, with oral capecitabine.
- **CAR**: Complete Anastomotic Ring; post-resection check for intact doughnut in anastomosis.
- **CEA**: Carcinoembryonic Antigen; blood tumor marker for monitoring colorectal cancer recurrence.
- **CNS**: Clinical Nurse Specialist; expert nurse providing support and coordination for cancer patients.
- **CR**: Complete Response; no detectable tumor after treatment, e.g., post-CRT.
- **CRM**: Circumferential Resection Margin; distance from tumor to surgical edge in rectum, critical for recurrence risk.
- **CRT**: Chemoradiotherapy; combined chemotherapy and radiotherapy, often neoadjuvant for rectal cancer.
- **CT**: Computed Tomography; imaging for staging and metastasis detection.
- **DTT**: Decision to Treat; point when MDT agrees on treatment plan, starting timed pathways.
- **EBRT**: External Beam Radiotherapy; standard radiation delivery from outside the body.
- **EGFR**: Epidermal Growth Factor Receptor; protein targeted by drugs like cetuximab in RAS-wild-type cancers.
- **ELAPE**: Extralevator Abdominoperineal Excision; extended APE for low rectal tumors to reduce positive margins.
- **EMVI**: Extramural Vascular Invasion; tumor in veins outside bowel wall, indicating higher metastasis risk.
- **ERUS**: Endorectal Ultrasound; imaging for early rectal tumor staging.
- **FDG**: Fluorodeoxyglucose; tracer in PET-CT for detecting metabolically active tumors.
- **Flexi sig**: Flexible Sigmoidoscopy; endoscopy examining rectum and sigmoid colon.
- **FOLFIRI**: Folinate + 5-FU + Irinotecan; chemotherapy for metastatic disease.
- **FOLFOX**: Folinate + 5-FU + Oxaliplatin; standard chemotherapy for colon/rectal cancer.
- **FOXTROT**: Fluorouracil, Oxaliplatin and Targeted Receptor pre-Operative Therapy; trial showing benefits of neoadjuvant chemo in colon cancer.
- **HER2**: Human Epidermal Growth Factor Receptor 2; amplification in some cancers, potential for targeted therapy.
- **ICD-10**: International Classification of Diseases, 10th Revision; coding system for diagnoses like C18-C20 for colorectal cancer.
- **ICV**: Ileocaecal Valve; landmark for complete colonoscopy.
- **IHC**: Immunohistochemistry; lab technique staining tissues for proteins like MMR.
- **ISP**: Intersphincteric Plane; anatomical space affecting sphincter-sparing surgery in low rectal cancer.
- **KRAS**: Kirsten Rat Sarcoma viral oncogene; mutations preclude anti-EGFR therapy.
- **MDT**: Multidisciplinary Team; group of specialists discussing cancer cases for treatment decisions.
- **MMR**: Mismatch Repair; DNA repair system; deficient status linked to MSI-H and immunotherapy eligibility.
- **MRI**: Magnetic Resonance Imaging; detailed imaging for rectal staging.
- **mrCRM**: MRI-assessed Circumferential Resection Margin; pre-treatment estimate.
- **mrEMVI**: MRI-assessed Extramural Vascular Invasion; imaging sign of vascular involvement.
- **mrN**: MRI-assessed Nodal stage; nodal involvement on MRI.
- **mrT**: MRI-assessed Tumor stage; local invasion on MRI.
- **MSI**: Microsatellite Instability; marker of DNA instability, related to MMR.
- **MSI-H**: Microsatellite Instability-High; subset eligible for immunotherapy.
- **N stage**: Nodal stage in TNM; indicates lymph node involvement.
- **nCRT**: Neoadjuvant Chemoradiotherapy; pre-surgery CRT.
- **NRAS**: Neuroblastoma Rat Sarcoma viral oncogene; mutations like KRAS affect therapy.
- **PET-CT**: Positron Emission Tomography-Computed Tomography; functional imaging for mets.
- **PR**: Partial Response; tumor shrinkage but not complete after treatment.
- **PSW**: Posterior Surgical Wall / Presacral Space; area behind rectum relevant for surgical planning.
- **RAS**: Rat Sarcoma oncogene family (KRAS/NRAS); wild-type required for anti-EGFR.
- **RFA**: Radiofrequency Ablation; heat-based destruction of tumors, e.g., liver mets.
- **SABR**: Stereotactic Ablative Radiotherapy; precise high-dose RT for mets.
- **SCRT**: Short-Course Radiotherapy; 5-fraction pre-op RT for rectal cancer.
- **SIRT**: Selective Internal Radiation Therapy; radioactive beads for liver mets.
- **SM1/SM2/SM3**: Submucosal invasion levels in early lesions; deeper increases node risk.
- **T stage**: Tumor stage in TNM; indicates primary tumor depth.
- **TAMIS**: Transanal Minimally Invasive Surgery; local excision for early rectal tumors.
- **TEM**: Transanal Endoscopic Microsurgery; technique for polyp/tumor removal.
- **TME**: Total Mesorectal Excision; standard rectal surgery to minimize recurrence.
- **TNM**: Tumor-Node-Metastasis; primary staging system for colorectal cancer.
- **TNT**: Total Neoadjuvant Therapy; all systemic treatment before surgery.
- **TWR**: Two-Week Rule; synonymous with 2WW for urgent referrals.
- **VEGF**: Vascular Endothelial Growth Factor; targeted by bevacizumab to inhibit blood supply.
- **W&W**: Watch and Wait; non-surgical surveillance after CR to neoadjuvant therapy.
- **62-day target**: NHS timeline from urgent referral to first treatment.

## Sources

- NICE guidelines: NG151 (Colorectal cancer, 2020, updated).
- ESMO guidelines: Colorectal cancer (2023, including early colon, locally advanced rectal, metastatic).
- NCCN guidelines: Colon Cancer and Rectal Cancer (Version 1.2024).
- ACPGBI: Position Statement on Locally Advanced Rectal Cancer (2016, updated).
- BSG guidelines: British Society of Gastroenterology colorectal cancer guidelines (2020).
- RCR: Royal College of Radiologists guidelines on imaging in colorectal cancer.
- Relevant trials: FOXTROT (Lancet 2023), RAPIDO (NEJM 2020), PRODIGE 23 (Lancet Oncol 2018), CAO/ARO/AIO-12 (JAMA Oncol 2020), ARISTOTLE (Lancet 2017), MERCURY (Radiology 2007).
- Databases: WHO fact sheets, American Cancer Society statistics (2026), PubMed/PMC for epidemiology and staging (e.g., AJCC 8th edition).
