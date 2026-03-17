# Clinician Questions - March 16 Session

These questions address specific ambiguities found during the baseline implementation phase.

## 1. Date Attribution Hierarchy
- **Patient Example:** AIDEN O'\''CONNOR (NHS: 9990000001)
- **Evidence Snippet:** `CT 29/02/2025: Mid rectal cancer...`
- **Question:** The MDT date is 07/03/2025. If multiple scan dates exist (e.g. CT and MRI mentioned in the same case), which date should be the primary date in the database?

## 2. Staging Notation Hierarchy
- **Patient Example:** ZIAD AL-FARSI (NHS: 9990000002)
- **Evidence Snippet:** `Staging: T3 N0 M0`
- **Question:** In this case, the *Integrated TNM Stage* is blank, but *Staging* says `T3 N0 M0`. Should students use the manual staging or prioritize the Integrated TNM field if present elsewhere?

## 3. Treatment Mapping (FOXTROT)
- **Patient Example:** (NHS: 9990000021)
- **Evidence Snippet:** `FOXTROT trial...`
- **Question:** How should a specific trial name like FOXTROT map to the standard treatment categories (TNT, nCRT, etc.) in the Excel spreadsheet?

## 4. Implicit Biopsy Dates
- **Patient Example:** AIDEN O'\''CONNOR (NHS: 9990000001)
- **Evidence Snippet:** `Colonoscopy noted - Histo: Adenocarcinoma.`
- **Question:** No biopsy date is explicitly listed. Is it clinically correct to assume the biopsy date is the same as the colonoscopy date (29/02/2025 inferred) unless stated otherwise?

## 5. MDT Decision Refinement
- **Patient Example:** AIDEN O'\''CONNOR (NHS: 9990000001)
- **Evidence Snippet:** `Outcome: MRI Rectum, PET CT. Rediscuss at MDT for formal staging...`
- **Question:** The outcome is often a paragraph with several steps (Investigations + Plan). Should the student extract only the first recommendation, the final decision, or the entire summary?

## 6. MRI Parameters (mrT / mrN)
- **Patient Example:** (NHS: 9990000003)
- **Evidence Snippet:** `MRI: mrT3c mrN1a mrEMVI positive...`
- **Question:** These specific parameters have their own columns. Is it acceptable to treat these as the definitive staging for the database even if the CT staging is slightly different?

