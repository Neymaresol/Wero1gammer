import unittest
from catalog_gates import CatalogCandidate, validate
BASE = dict(sku="GPU-123", tier="ouro", category="placa_video",
            supplier_authorized=True, stock_confirmed=True,
            warranty_confirmed=True, market_price_verified=True,
            supplier_total_brl="900.00", proposed_price_brl="1200.00")
class CatalogGateTests(unittest.TestCase):
    def test_valid_is_only_candidate(self):
        r=validate(CatalogCandidate(**BASE))
        self.assertTrue(r["eligible_for_review"])
        self.assertFalse(r["publish_enabled"])
        self.assertFalse(r["checkout_enabled"])
    def test_no_authorization(self):
        self.assertIn("supplier_not_authorized",validate(CatalogCandidate(**(BASE | {"supplier_authorized":False})))["reasons"])
    def test_no_stock(self):
        self.assertIn("stock_not_confirmed",validate(CatalogCandidate(**(BASE | {"stock_confirmed":False})))["reasons"])
    def test_bad_margin(self):
        self.assertIn("invalid_margin",validate(CatalogCandidate(**(BASE | {"proposed_price_brl":"800"})))["reasons"])
    def test_bad_tier(self):
        self.assertIn("invalid_tier",validate(CatalogCandidate(**(BASE | {"tier":"diamante"})))["reasons"])
    def test_nan(self):
        self.assertIn("invalid_margin",validate(CatalogCandidate(**(BASE | {"proposed_price_brl":"NaN"})))["reasons"])
if __name__=="__main__": unittest.main()
