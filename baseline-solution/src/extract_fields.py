import re

def extract_initials(name):
    if not name: return ""
    # Remove junk
    name = re.sub(r'(?:Hospital|NHS|Number|Age|Years|Male|Female|[\d\:\(\)])', '', name, flags=re.IGNORECASE).strip()
    parts = name.split()
    return "".join([p[0].upper() for p in parts if p])

def find_marker(text, marker, pattern=r'(\d+)'):
    """
    Finds a value near a marker like (c) or (d).
    Example: Hospital Number: 9990001(d)
    """
    # Try finding it just before the marker
    match = re.search(pattern + r'\s*\(' + marker + r'\)', text)
    if match: return match.group(1)
    
    # Try finding it a bit further before the marker
    match = re.search(pattern + r'.{1,20}\(' + marker + r'\)', text, re.DOTALL)
    if match: return match.group(1)

    return ""

def extract_case_fields(case_data, doc_date=None):
    table = case_data['table']
    fields = {}
    fields['1st MDT: date(i)'] = doc_date

    seen_texts = set()
    all_cells = []
    for row in table.rows:
        for cell in row.cells:
            cell_text = "\n".join([p.text for p in cell.paragraphs]).strip()
            if cell_text and cell_text not in seen_texts:
                all_cells.append(cell_text)
                seen_texts.add(cell_text)
    
    full_text = "\n".join(all_cells)

    # 2. Patient Demographics using markers
    fields['Demographics: \nDOB(a)'] = find_marker(full_text, 'a', r'(\d{2}/\d{2}/\d{4})')
    
    # Name (b)
    name_raw = find_marker(full_text, 'b', r'([A-Z\s\']+)')
    fields['Demographics: Initials(b)'] = extract_initials(name_raw)

    fields['Demographics: MRN(c)'] = find_marker(full_text, 'c', r'(\d+)') # Wait, source has (c) for NHS and (d) for Hospital? 
    # Let's re-verify from DEBUG:
    # Hospital Number: 9990001(d)
    # NHS Number: 9990000001(c)
    
    # Actually, the prototype says:
    # MRN(c)
    # NHS number(d)
    
    # This means we should map source (d) -> MRN(c) and source (c) -> NHS(d)
    fields['Demographics: MRN(c)'] = find_marker(full_text, 'd', r'(\d+)')
    fields['Demographics: \nNHS number(d)'] = find_marker(full_text, 'c', r'(\d+)')
    
    gender_raw = find_marker(full_text, 'e', r'(Male|Female)')
    fields['Demographics: \nGender(e)'] = gender_raw

    # 3. Clinical Fields
    diag_match = re.search(r'Diagnosis:\s*(.*?)(?:\n|$)', full_text)
    fields['Histology: Biopsy result(g)'] = diag_match.group(1).strip() if diag_match else ""

    # Histology Date (g)
    # Often found in the Outcome or Clinical Details as "Histo: Adenocarcinoma. MMR deficient" 
    # but the prototype has a specific "Histology: Biopsy date(g)" field.
    # In the DOCX, I don't see a clear "Biopsy Date(g)" marker in the first few cases.
    # Let's search for any date in the Staging & Diagnosis area.

    # Staging: T3 N0 M0
    staging_match = re.search(r'Staging:\s*([TNM\d\s]+)', full_text)
    if staging_match:
        staging_str = staging_match.group(1).strip()
        # Extract T, N, M components
        t_comp = re.search(r'T(\d[a-z]?)', staging_str)
        n_comp = re.search(r'N(\d[a-z]?)', staging_str)
        m_comp = re.search(r'M(\d[a-z]?)', staging_str)
        if t_comp: fields['Baseline CT: T(h)'] = t_comp.group(1)
        if n_comp: fields['Baseline CT: N(h)'] = n_comp.group(1)
        if m_comp: fields['Baseline CT: M(h)'] = m_comp.group(1)

    endo_match = re.search(r'(?:Colonoscopy|Flexi\s*Sig)\s*:\s*(.*?)(?:\n\n|\n[A-Z]|$)', full_text, re.DOTALL)
    fields['Endoscopy: Findings(f)'] = endo_match.group(1).strip() if endo_match else ""

    outcome_match = re.search(r'Outcome:\s*(.*?)(?:\n|$)', full_text)
    fields['MDT (after 6 week: Decision '] = outcome_match.group(1).strip() if outcome_match else ""

    if "MMR deficient" in full_text:
        fields['Histology: \nMMR status(g/h)'] = "Deficient"
    elif "MMR proficient" in full_text:
        fields['Histology: \nMMR status(g/h)'] = "Proficient"

    return fields
