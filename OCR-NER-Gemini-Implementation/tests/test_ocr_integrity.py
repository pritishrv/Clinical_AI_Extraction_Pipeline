import os
import json
import unittest

class TestOCRIntegrity(unittest.TestCase):
    def setUp(self):
        self.raw_json_dir = "output/json_raw"
        
    def test_json_output_exists(self):
        """
        Verify that Stage 1 produced raw JSON output.
        """
        if os.path.exists(self.raw_json_dir):
            files = [f for f in os.listdir(self.raw_json_dir) if f.endswith(".json")]
            self.assertGreater(len(files), 0, "No raw JSON files found in output/json_raw.")
        else:
            self.skipTest("output/json_raw directory does not exist. Run Stage 1 first.")

    def test_json_structure(self):
        """
        Verify that the raw JSON has the expected keys.
        """
        if os.path.exists(self.raw_json_dir):
            files = [f for f in os.listdir(self.raw_json_dir) if f.endswith(".json")]
            if files:
                with open(os.path.join(self.raw_json_dir, files[0]), "r") as f:
                    data = json.load(f)
                    self.assertIn("case_index", data)
                    self.assertIn("raw_text", data)
                    self.assertIn("ocr_metadata", data)
        else:
            self.skipTest("output/json_raw directory does not exist.")

if __name__ == "__main__":
    unittest.main()
