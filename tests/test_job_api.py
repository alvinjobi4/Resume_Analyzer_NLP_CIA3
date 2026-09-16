import unittest
import json
from pathlib import Path
from services.job_api import normalize_job

class TestJobApi(unittest.TestCase):

    def test_normalize_job_structure(self):
        sample_path = Path(__file__).resolve().parent.parent / "sample_data" / "sample_job.json"
        with open(sample_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        raw_job = data["data"][0]
        normalized = normalize_job(raw_job)

        self.assertEqual(normalized["title"], "Machine Learning Engineer")
        self.assertEqual(normalized["company"], "ABC Technologies")
        self.assertIn("Bengaluru", normalized["location"])
        self.assertIn("$90,000", normalized["salary"])
        self.assertEqual(normalized["source"], "JSearch API")
        self.assertTrue(len(normalized["description"]) > 50)

    def test_normalize_job_with_missing_fields(self):
        sparse_raw = {
            "job_id": "test-123"
        }
        normalized = normalize_job(sparse_raw)
        self.assertEqual(normalized["job_id"], "test-123")
        self.assertEqual(normalized["title"], "Untitled Position")
        self.assertEqual(normalized["company"], "Unknown Employer")
        self.assertEqual(normalized["salary"], "Not provided")
        self.assertEqual(normalized["description"], "Not provided")

if __name__ == "__main__":
    unittest.main()
