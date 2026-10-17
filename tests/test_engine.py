import unittest
from engine import D, SupplierQuote, MarketQuote, evaluate, tier

class PricingTests(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual(tier("computer", D("6000")), "PRATA")
        self.assertEqual(tier("computer", D("10000")), "OURO")
        self.assertEqual(tier("computer", D("20000")), "PREMIUM")
        self.assertEqual(tier("gpu", D("20000")), "AVULSO")

    def test_cheapest_landed_cost(self):
        suppliers = [SupplierQuote("cheap expensive freight", "GPU1", D("3500"), D("600"), True, True, True),
                     SupplierQuote("best total", "GPU1", D("3700"), D("100"), True, True, True)]
        result = evaluate("GPU1", "gpu", suppliers, [MarketQuote("GPU1", D("5000"), True)])
        self.assertEqual(result["supplier"], "best total")
        self.assertEqual(result["status"], "CANDIDATE_ONLY")
        self.assertFalse(result["checkout_enabled"])

    def test_reject_unauthorized(self):
        quotes = [SupplierQuote("X", "GPU1", D("1000"), D("10"), True, False, True)]
        self.assertEqual(evaluate("GPU1", "gpu", quotes, [MarketQuote("GPU1", D("5000"), True)])["status"], "BLOCKED")

    def test_reject_loss(self):
        quotes = [SupplierQuote("X", "GPU1", D("4500"), D("100"), True, True, True)]
        self.assertEqual(evaluate("GPU1", "gpu", quotes, [MarketQuote("GPU1", D("4600"), True)])["status"], "BLOCKED")

    def test_reject_missing_market(self):
        quotes = [SupplierQuote("X", "GPU1", D("1000"), D("10"), True, True, True)]
        self.assertEqual(evaluate("GPU1", "gpu", quotes, [])["status"], "BLOCKED")

    def test_reject_nan(self):
        with self.assertRaises(ValueError):
            D("NaN")

    def test_reject_negative_shipping(self):
        quotes = [SupplierQuote("X", "GPU1", D("1000"), D("-10"), True, True, True)]
        self.assertEqual(evaluate("GPU1", "gpu", quotes, [MarketQuote("GPU1", D("5000"), True)])["status"], "BLOCKED")

if __name__ == "__main__":
    unittest.main()
