import json
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
import app as service


class TestMLService(unittest.TestCase):
    def test_artifacts_exist(self):
        self.assertTrue(Path("artifacts/model.joblib").exists())
        self.assertTrue(Path("artifacts/metrics.json").exists())

    def test_metrics_endpoint(self):
        client = TestClient(service.app)
        res = client.get("/metrics")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["student_id"], "SP23-BAI-044")
        self.assertGreaterEqual(data["training_rows"], 100)
        self.assertGreater(data["accuracy"], 0.5)

    def test_predict_endpoint(self):
        config = json.loads(Path("config.json").read_text())
        sample = {feat: 0.5 for feat in config["features"]}
        client = TestClient(service.app)
        res = client.post("/predict", json={"records": [sample]})
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertIn("predictions", body)
        self.assertEqual(len(body["predictions"]), 1)


if __name__ == "__main__":
    unittest.main()
