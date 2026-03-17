import unittest
from src.load_docx import load_cases
from src.extract_fields import extract_case_fields
import os

class TestStandardSolution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docx_path = "../data/hackathon-mdt-outcome-proformas.docx"
        if not os.path.exists(cls.docx_path):
            raise unittest.SkipTest("DOCX not found")
        cls.cases, cls.doc = load_cases(cls.docx_path)

    def test_case_count(self):
        # We expect exactly 50 cases in this synthetic dataset
        self.assertEqual(len(self.cases), 50)

    def test_demographics_extraction(self):
        # Test extraction on the first case
        fields = extract_case_fields(self.cases[0])
        self.assertIn('Demographics: Initials(b)', fields)
        self.assertIn('Demographics: \nNHS number(d)', fields)
        self.assertGreater(len(fields['Demographics: \nNHS number(d)']), 0)

if __name__ == '__main__':
    unittest.main()
