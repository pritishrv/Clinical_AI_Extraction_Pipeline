"""
Claude extractor.

Improvements over the Codex extractor:
- Endoscopy date: handles `TYPE DATE:` pattern (date immediately after type name)
- Histology biopsy date: inferred from colonoscopy/flexi-sig date when findings
  mention cancer or biopsy (defensible since biopsy is taken during the procedure)
- CT date: broadened to match `CT abdomen`, `CT pelvis`, and other CT qualifiers
- MDT decision: extracts text after explicit "Outcome:" keyword when present,
  avoiding mixing imaging summaries with the actionable decision
"""
import re


DATE_PATTERN = r"\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}"

# Endash (U+2013) appears in the source document alongside regular hyphens.
_SEP = r"[:\-\u2013]"


def _dedupe_preserve_order(values):
    seen = set()
    result = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            result.append(cleaned)
            seen.add(cleaned)
    return result


def _row_text(table, row_index):
    cells = []
    for cell in table.rows[row_index].cells:
        cell_text = " | ".join(
            paragraph.text.strip() for paragraph in cell.paragraphs if paragraph.text.strip()
        )
        if cell_text:
            cells.append(cell_text)
    return " | ".join(_dedupe_preserve_order(cells))


def _clean_date(value):
    if not value:
        return ""
    value = value.strip()
    parts = re.split(r"[/\-\.]", value)
    if len(parts) != 3:
        return ""
    day, month, year = parts
    if len(year) == 2:
        year = f"20{year}"
    return f"{day.zfill(2)}/{month.zfill(2)}/{year}"


def _extract_name(demo_text):
    patterns = [
        r"NHS Number:\s*\d+\s*\|+\s*Name:\s*([^|]+?)\s*\|+\s*(?:Gender|Male|Female|DOB)",
        r"NHS Number:\s*\d+\s*(?:\(c\))?\s*\|+\s*([^|]+?)\s*\|+\s*(?:Male|Female|Gender:)",
    ]
    for pattern in patterns:
        match = re.search(pattern, demo_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def _extract_initials(name):
    cleaned = re.sub(r"^Name:\s*", "", name, flags=re.IGNORECASE).strip()
    cleaned = cleaned.replace("-", " ")
    parts = [part for part in cleaned.split() if part]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0][0].upper()
    return f"{parts[0][0].upper()}{parts[-1][0].upper()}"


def _extract_first(pattern, text, flags=0):
    match = re.search(pattern, text, flags)
    return match.group(1).strip() if match else ""


def _extract_gender(text):
    match = re.search(r"\b(Male|Female)\b", text, re.IGNORECASE)
    return match.group(1).title() if match else ""


def _extract_previous_cancer(clinical_text):
    lowered = clinical_text.lower()
    positive_patterns = {
        "lymphoma": "lymphoma",
        "breast cancer": "breast cancer",
        "prostate cancer": "prostate cancer",
        "head and neck cancer": "head and neck cancer",
    }
    for needle, label in positive_patterns.items():
        if needle in lowered:
            return "Yes", label

    if re.search(r"\b(previous|prior|history of|known)\b.*\bcancer\b", lowered):
        snippet = _extract_first(r"\b(previous|prior|history of|known)\b[^|]{0,80}", clinical_text, re.IGNORECASE)
        return "Yes", snippet or "previous cancer"

    return "No", "N/A"


def _extract_diagnosis(diag_text, outcome_text):
    diagnosis = _extract_first(r"Diagnosis:\s*([^|]+)", diag_text, re.IGNORECASE)
    if diagnosis:
        return diagnosis

    for segment in [part.strip() for part in outcome_text.split("|") if part.strip()]:
        if re.search(r"adenocarcinoma|adenoma|dysplasia|carcinoma", segment, re.IGNORECASE):
            cleaned = re.sub(r"^(Colonoscopy|Flexi sig)\s*:\s*", "", segment, flags=re.IGNORECASE)
            return cleaned.strip()
    return ""


def _extract_mmr(text):
    if re.search(r"\bMMR\s+deficient\b|\bdeficient\s+MMR\b", text, re.IGNORECASE):
        return "Deficient"
    if re.search(r"\bMMR\s+proficient\b|\bproficient\s+MMR\b", text, re.IGNORECASE):
        return "Proficient"
    return ""


def _extract_endoscopy(text):
    """
    Extract endoscopy type, date, and findings from combined clinical/outcome text.

    Handles three source patterns:
    1.  TYPE DATE: findings  (e.g. "Flexi sig 20/10/2024: rectal cancer ...")
    2.  TYPE on DATE: findings  (e.g. "Colonoscopy on 01/01/2024: ...")
    3.  TYPE: findings  (no date present)

    Returns a dict with the three endoscopy fields.
    """
    _ENDO_TYPE = r"((?:completion |repeat )?(?:colonoscopy|flexi\s*sig|sigmoidoscopy))"
    _DATE = r"(" + DATE_PATTERN + r")"
    _SEP_OPT = r"\s*" + _SEP + r"?\s*"

    # Pattern 1: TYPE DATE [sep] findings
    p_date_direct = _ENDO_TYPE + r"\s+" + _DATE + _SEP_OPT + r"([^|]*)"
    # Pattern 2: TYPE on DATE [sep] findings
    p_date_on = _ENDO_TYPE + r"\s+on\s+" + _DATE + _SEP_OPT + r"([^|]*)"
    # Pattern 3: TYPE [sep] findings (no date)
    p_no_date = _ENDO_TYPE + r"\s*" + _SEP + r"\s*([^|]+)"

    for pattern, has_date in [
        (p_date_direct, True),
        (p_date_on, True),
        (p_no_date, False),
    ]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_type = match.group(1)
            if has_date:
                raw_date = match.group(2)
                findings = match.group(3).strip()
            else:
                raw_date = ""
                findings = match.group(2).strip()

            endo_type = (
                "flexi sig"
                if re.search(r"flexi|sigmoidoscopy", raw_type, re.IGNORECASE)
                else "Colonoscopy complete"
            )
            return {
                "Endoscopy: date(f)": _clean_date(raw_date),
                "Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) ": endo_type,
                "Endoscopy: Findings(f)": findings,
                "_endoscopy_date_raw": raw_date,
                "_endoscopy_has_cancer": bool(
                    re.search(r"adenocarcinoma|carcinoma|cancer|biopsy", findings, re.IGNORECASE)
                ),
            }

    return {
        "Endoscopy: date(f)": "",
        "Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) ": "",
        "Endoscopy: Findings(f)": "",
        "_endoscopy_date_raw": "",
        "_endoscopy_has_cancer": False,
    }


def _infer_histology_date(endoscopy_result, text):
    """
    Return a defensible histology biopsy date when the evidence supports it.

    A biopsy date is inferred from the endoscopy date only when:
    - a dated endoscopy was found, AND
    - the findings for that endoscopy mention cancer/carcinoma/biopsy

    This is defensible because a biopsy is taken during the endoscopy procedure.
    In all other cases the field is left blank rather than guessed.
    """
    if endoscopy_result.get("_endoscopy_date_raw") and endoscopy_result.get("_endoscopy_has_cancer"):
        return _clean_date(endoscopy_result["_endoscopy_date_raw"])

    # Explicit biopsy-date phrasing in the text
    match = re.search(
        r"(?:biopsy|histo(?:logy)?)\s*(?:on|date)?\s*[:\-]?\s*(" + DATE_PATTERN + r")",
        text,
        re.IGNORECASE,
    )
    return _clean_date(match.group(1)) if match else ""


def _extract_staging_components(text):
    result = {}

    t_match = re.search(r"(?:\b(?:mr|ct|c|p)?T)\s*([0-4](?:[a-d]|sm\d(?:/\d)?)?)", text, re.IGNORECASE)
    n_match = re.search(r"(?:\b(?:mr|ct|c|p)?N)\s*([0-3](?:[a-c])?)", text, re.IGNORECASE)
    m_match = re.search(r"(?:\b(?:mr|ct|c|p)?M)\s*([0-1](?:[a-c])?)", text, re.IGNORECASE)

    if t_match:
        result["T"] = t_match.group(1)
    if n_match:
        result["N"] = n_match.group(1)
    if m_match:
        result["M"] = m_match.group(1)

    emvi_match = re.search(r"EMVI\s*[:\-]?\s*(positive|negative|clear|unsafe|\+|-)", text, re.IGNORECASE)
    if emvi_match:
        value = emvi_match.group(1)
        result["EMVI"] = {"+": "positive", "-": "negative"}.get(value, value)

    crm_match = re.search(r"CRM(?:/ISP)?\s*[:\-]?\s*(clear|unsafe|threatened|involved)", text, re.IGNORECASE)
    if crm_match:
        result["CRM"] = crm_match.group(1)

    psw_match = re.search(r"PSW\s*[:\-]?\s*(clear|unsafe|\+|-)", text, re.IGNORECASE)
    if psw_match:
        value = psw_match.group(1)
        result["PSW"] = {"+": "positive", "-": "negative"}.get(value, value)

    return result


def _extract_modality_segment(text, modality_pattern):
    segments = [segment.strip() for segment in text.split("|") if segment.strip()]
    for segment in segments:
        if re.search(modality_pattern, segment, re.IGNORECASE):
            return segment
    return ""


def _extract_ct_fields(text, staging_text):
    """
    Find the first CT staging segment and extract date and staging values.

    Expanded over the Codex version to handle:
    - CT TAP, CT colonography (existing)
    - CT abdomen, CT pelvis, CT thorax, CT chest (new)
    - CT [qualifier] on DATE (new)
    - PET-CT is excluded as it is a different modality
    """
    # Match CT segments but not PET-CT
    ct_segment = _extract_modality_segment(text, r"(?<!PET[‑\-])\bCT\b(?!\s*scan\b)")
    if not ct_segment:
        ct_segment = _extract_modality_segment(text, r"\bCT\b")

    # Broadened date pattern: CT [qualifier words up to 25 chars] [on] DATE
    date = _extract_first(
        r"\bCT(?:\s+(?:TAP|abdomen|pelvis|thorax|chest|colonography|[a-z]+))?"
        r"(?:\s+on)?\s+(" + DATE_PATTERN + r")",
        ct_segment,
        re.IGNORECASE,
    )

    staging_source = ct_segment or staging_text
    staging = _extract_staging_components(staging_source)

    incidental_detail = ""
    incidental_flag = ""
    incidental_match = re.search(r"incidental ([^|]+)", ct_segment, re.IGNORECASE)
    if incidental_match:
        incidental_flag = "Y"
        incidental_detail = incidental_match.group(1).strip()

    if re.search(r"no metastases|no distant metastases|no mets|no distant disease|no liver metastases", ct_segment, re.IGNORECASE):
        m_value = "0"
    elif re.search(r"metastases|metastasis|metastatic|lung metastases|liver lesion", ct_segment, re.IGNORECASE):
        m_value = staging.get("M") or "1"
    else:
        m_value = staging.get("M", "")

    return {
        "Baseline CT: Date(h)": _clean_date(date),
        "Baseline CT: T(h)": staging.get("T", ""),
        "Baseline CT: N(h)": staging.get("N", ""),
        "Baseline CT: EMVI(h)": staging.get("EMVI", ""),
        "Baseline CT: M(h)": m_value,
        "Baseline CT: Incidental findings requiring follow up? Y/N(h)": incidental_flag,
        "Baseline CT: Detail incidental finding(h)": incidental_detail,
    }


def _extract_mri_fields(text):
    mri_segment = _extract_modality_segment(text, r"\bMR(?:I| rectum)\b")
    date = _extract_first(
        r"\bMR(?:I| rectum|I pelvis|I stage)?(?: [^:|]*)?(?: on)?\s*(" + DATE_PATTERN + r")",
        mri_segment,
        re.IGNORECASE,
    )
    staging = _extract_staging_components(mri_segment)
    return {
        "Baseline MRI: date(h)": _clean_date(date),
        "Baseline MRI: mrT(h)": staging.get("T", ""),
        "Baseline MRI: mrN(h)": staging.get("N", ""),
        "Baseline MRI: mrEMVI(h)": staging.get("EMVI", ""),
        "Baseline MRI: mrCRM(h)": staging.get("CRM", ""),
        "Baseline MRI: mrPSW(h)": staging.get("PSW", ""),
    }


def _extract_treatment_approach(outcome_text):
    lowered = outcome_text.lower()
    if "foxtrot" in lowered:
        return "downstaging chemotherapy"
    if "crt" in lowered or "chemoradiotherapy" in lowered:
        return "downstaging nCRT"
    if "watch and wait" in lowered:
        return "Papillon +/- EBRT"
    if re.search(r"surgery|hemicolectomy|elape|surgical review", lowered):
        return "straight to surgery"
    return ""


def _normalize_mdt_decision(outcome_text):
    """
    Extract the actionable MDT decision from the outcome row.

    Strategy:
    1. If an explicit "Outcome:" label is present, return only the text that follows it.
    2. Otherwise return the full outcome text unchanged (conservative fallback).

    This avoids mixing imaging summaries and histology paragraphs with the
    decision when they appear together in the same outcome cell.
    """
    outcome_match = re.search(r"\bOutcome\s*:\s*(.+)", outcome_text, re.IGNORECASE | re.DOTALL)
    if outcome_match:
        decision = outcome_match.group(1).strip()
        # Trim any trailing pipe-separated fragments that are actually imaging
        decision = re.split(r"\s*\|\s*(?:CT|MRI?|PET)\b", decision, flags=re.IGNORECASE)[0].strip()
        return decision
    return outcome_text.strip()


def extract_case_fields_claude(case_data, doc_date=None):
    table = case_data["table"]

    demo_text = _row_text(table, 1)
    diagnosis_text = _row_text(table, 3)
    staging_text = _row_text(table, 3)
    clinical_text = _row_text(table, 5)
    outcome_text = _row_text(table, 7)
    combined_text = " | ".join([demo_text, diagnosis_text, clinical_text, outcome_text])

    name = _extract_name(demo_text)
    previous_cancer, previous_cancer_site = _extract_previous_cancer(clinical_text)
    endoscopy = _extract_endoscopy(f"{clinical_text} | {outcome_text}")
    histology_date = _infer_histology_date(endoscopy, f"{clinical_text} | {outcome_text}")
    ct_fields = _extract_ct_fields(f"{clinical_text} | {outcome_text}", staging_text)
    mri_fields = _extract_mri_fields(f"{clinical_text} | {outcome_text}")

    # Strip internal helper keys before returning
    endoscopy_public = {k: v for k, v in endoscopy.items() if not k.startswith("_")}

    fields = {
        "Demographics: \nDOB(a)": _clean_date(
            _extract_first(r"(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4})\s*(?:\(a\)|Age:|Years)", demo_text, re.IGNORECASE)
        ),
        "Demographics: Initials(b)": _extract_initials(name),
        "Demographics: MRN(c)": _extract_first(r"Hospital Number:\s*(\d+)", demo_text, re.IGNORECASE),
        "Demographics: \nNHS number(d)": _extract_first(r"NHS Number:\s*(\d+)", demo_text, re.IGNORECASE),
        "Demographics: \nGender(e)": _extract_gender(demo_text),
        "Demographics:\nPrevious cancer \n(y, n) \nif yes, where(f)": previous_cancer,
        "Demographics: \nState site of previous cancer(f)": previous_cancer_site,
        "Histology: Biopsy result(g)": _extract_diagnosis(diagnosis_text, outcome_text),
        "Histology: Biopsy date(g)": histology_date,
        "Histology: \nMMR status(g/h)": _extract_mmr(combined_text),
        "1st MDT: date(i)": doc_date or "",
        "1st MDT: Treatment approach \n(TNT, downstaging chemotherapy, downstaging nCRT, downstaging shortcourse RT, Papillon +/- EBRT, straight to surgery(h)": _extract_treatment_approach(outcome_text),
        "MDT (after 6 week: Decision ": _normalize_mdt_decision(outcome_text),
    }

    fields.update(endoscopy_public)
    fields.update(mri_fields)
    fields.update(ct_fields)

    return fields
