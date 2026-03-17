"""
Targeted tests for the Claude extractor.

Tests focus on the specific improvements over the Codex extractor:
- endoscopy date extraction from TYPE DATE: patterns
- histology biopsy date inferred from colonoscopy date
- broadened CT date extraction
- MDT decision normalization
"""
import unittest

from src.claude_extract_fields import extract_case_fields_claude
from src.load_docx import load_cases


class TestClaudeImplementation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases, cls.doc = load_cases("../data/hackathon-mdt-outcome-proformas.docx")

    # --- demographics (should still pass) ---

    def test_case_zero_demographics(self):
        fields = extract_case_fields_claude(self.cases[0], doc_date="07/03/2025")
        self.assertEqual(fields["Demographics: Initials(b)"], "AO")
        self.assertEqual(fields["Demographics: MRN(c)"], "9990001")
        self.assertEqual(fields["Demographics: \nNHS number(d)"], "9990000001")
        self.assertEqual(fields["Demographics:\nPrevious cancer \n(y, n) \nif yes, where(f)"], "No")

    def test_case_one_previous_cancer_and_mri(self):
        fields = extract_case_fields_claude(self.cases[1], doc_date="07/03/2025")
        self.assertEqual(fields["Demographics:\nPrevious cancer \n(y, n) \nif yes, where(f)"], "Yes")
        self.assertEqual(fields["Demographics: \nState site of previous cancer(f)"], "lymphoma")
        self.assertEqual(fields["Baseline MRI: mrT(h)"], "3c")
        self.assertEqual(fields["Baseline MRI: mrN(h)"], "1c")

    # --- endoscopy date (new) ---

    def test_case_40_flexi_sig_date(self):
        """Case 40 has 'Flexi sig 20/10/2024: ...' — date follows type directly."""
        fields = extract_case_fields_claude(self.cases[40], doc_date="07/03/2025")
        self.assertEqual(fields["Endoscopy: date(f)"], "20/10/2024")
        self.assertIn("flexi sig", fields[
            "Endosopy type: flexi sig, incomplete colonoscopy, colonoscopy complete - if gets to ileocecal valve(f) "
        ].lower())

    def test_case_35_colonoscopy_date(self):
        """Case 35 has 'Colonoscopy 01/01/2024: ...' — date follows type directly."""
        fields = extract_case_fields_claude(self.cases[35], doc_date="07/03/2025")
        self.assertEqual(fields["Endoscopy: date(f)"], "01/01/2024")

    def test_case_0_colonoscopy_no_date(self):
        """Case 0 has 'Colonoscopy: ...' with no date — date field must remain blank."""
        fields = extract_case_fields_claude(self.cases[0], doc_date="07/03/2025")
        self.assertEqual(fields["Endoscopy: date(f)"], "")

    # --- histology biopsy date inferred from colonoscopy (new) ---

    def test_case_40_biopsy_date_inferred(self):
        """Case 40: flexi sig with cancer findings → biopsy date = flexi sig date."""
        fields = extract_case_fields_claude(self.cases[40], doc_date="07/03/2025")
        self.assertEqual(fields["Histology: Biopsy date(g)"], "20/10/2024")

    def test_case_0_biopsy_date_not_inferred_without_endo_date(self):
        """Case 0: colonoscopy with no date → biopsy date must stay blank."""
        fields = extract_case_fields_claude(self.cases[0], doc_date="07/03/2025")
        self.assertEqual(fields["Histology: Biopsy date(g)"], "")

    # --- CT date (broadened) ---

    def test_ct_date_from_ct_abdomen_on_pattern(self):
        """
        Cases like 'CT abdomen on 02/01/2024:' must now yield a CT date.
        We check that at least one of the known previously-missed cases gets a date.
        """
        # Case 18 has 'CT abdomen on 02/01/2024:' which the Codex pattern missed
        fields = extract_case_fields_claude(self.cases[18], doc_date="07/03/2025")
        self.assertEqual(fields["Baseline CT: Date(h)"], "02/01/2024")

    def test_ct_date_case_23(self):
        """Case 23 has 'CT abdomen on 03/01/2025:' — must be captured."""
        fields = extract_case_fields_claude(self.cases[23], doc_date="07/03/2025")
        self.assertEqual(fields["Baseline CT: Date(h)"], "03/01/2025")

    def test_ct_date_case_28(self):
        """Case 28 has 'CT abdomen on 07/12/2024:' — must be captured."""
        fields = extract_case_fields_claude(self.cases[28], doc_date="07/03/2025")
        self.assertEqual(fields["Baseline CT: Date(h)"], "07/12/2024")

    # --- MDT decision normalization (new) ---

    def test_case_3_outcome_after_outcome_keyword(self):
        """Case 3 has 'Outcome: to see surgeon ...' — extracted value must start there."""
        fields = extract_case_fields_claude(self.cases[3], doc_date="07/03/2025")
        decision = fields["MDT (after 6 week: Decision "]
        self.assertIn("surgeon", decision.lower())
        # Should not contain the MRI summary
        self.assertNotIn("Persistent low signal", decision)

    def test_case_4_simple_outcome_preserved(self):
        """Case 4 has a simple single-sentence outcome — must be preserved unchanged."""
        fields = extract_case_fields_claude(self.cases[4], doc_date="07/03/2025")
        self.assertIn("surgical review", fields["MDT (after 6 week: Decision "].lower())


if __name__ == "__main__":
    unittest.main()
