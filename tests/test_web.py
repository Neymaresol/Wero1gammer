import unittest
from fastapi.testclient import TestClient
from app import app

class WebSmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_home_is_demo_only(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Wero1Gammer", response.text)
        self.assertIn("Sem ofertas verificadas", response.text)

    def test_health_blocks_checkout(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["version"], "0.1.1-dev")
        self.assertFalse(response.json()["checkout_enabled"])

    def test_missing_quotes_fail_closed(self):
        response = self.client.post("/api/pricing/evaluate",json={"sku":"GPU1","category":"gpu","suppliers":[],"market":[]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "BLOCKED")

if __name__ == "__main__":
    unittest.main()
