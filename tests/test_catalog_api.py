import unittest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
GOOD = {
    "sku": "GPU-123", "tier": "ouro", "category": "placa_video",
    "supplier_authorized": True, "stock_confirmed": True,
    "warranty_confirmed": True, "market_price_verified": True,
    "supplier_total_brl": "900.00", "proposed_price_brl": "1200.00",
}
class CatalogApiTests(unittest.TestCase):
    def test_eligible_not_published(self):
        r=client.post("/api/catalog/validate", json=GOOD)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.json()["eligible_for_review"])
        self.assertFalse(r.json()["publish_enabled"])
    def test_unverified_supplier_blocked(self):
        r=client.post("/api/catalog/validate", json=GOOD | {"supplier_authorized": False})
        self.assertIn("supplier_not_authorized", r.json()["reasons"])
    def test_health_disables_checkout(self):
        r=client.get("/health")
        self.assertFalse(r.json()["checkout_enabled"])
        self.assertFalse(r.json()["publication_enabled"])
if __name__ == "__main__": unittest.main()
