import unittest

from src.codex_extract_fields import extract_case_fields_codex
from src.load_docx import load_cases


class TestCodexImplementation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases, cls.doc = load_cases("../data/hackathon-mdt-outcome-proformas.docx")

    def test_case_zero_demographics(self):
        fields = extract_case_fields_codex(self.cases[0], doc_date="07/03/2025")
        self.assertEqual(fields["Demographics: Initials(b)"], "AO")
        self.assertEqual(fields["Demographics: MRN(c)"], "9990001")
        self.assertEqual(fields["Demographics: \nNHS number(d)"], "9990000001")
        self.assertEqual(fields["Demographics:\nPrevious cancer \n(y, n) \nif yes, where(f)"], "No")

    def test_case_one_previous_cancer_and_mri(self):
        fields = extract_case_fields_codex(self.cases[1], doc_date="07/03/2025")
        self.assertEqual(fields["Demographics:\nPrevious cancer \n(y, n) \nif yes, where(f)"], "Yes")
        self.assertEqual(fields["Demographics: \nState site of previous cancer(f)"], "lymphoma")
        self.assertEqual(fields["Baseline MRI: mrT(h)"], "3c")
        self.assertEqual(fields["Baseline MRI: mrN(h)"], "1c")


if __name__ == "__main__":
    unittest.main()
