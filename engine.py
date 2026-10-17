from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def D(value):
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("invalid monetary value")
    if not d.is_finite():
        raise ValueError("non-finite monetary value")
    return d

@dataclass(frozen=True)
class SupplierQuote:
    supplier: str
    sku: str
    cost: Decimal
    shipping: Decimal
    available: bool
    authorized: bool
    warranty_ok: bool

@dataclass(frozen=True)
class MarketQuote:
    sku: str
    price: Decimal
    verified: bool

@dataclass(frozen=True)
class PricingPolicy:
    tax_rate: Decimal = D("0.08")
    payment_rate: Decimal = D("0.04")
    warranty_reserve_rate: Decimal = D("0.02")
    fixed_cost: Decimal = D("20")
    minimum_profit: Decimal = D("80")
    discount_to_market: Decimal = D("0.02")

def tier(category, price):
    if category.lower() != "computer":
        return "AVULSO"
    return "PRATA" if price < D("7000") else "OURO" if price <= D("18000") else "PREMIUM"

def evaluate(sku, category, suppliers, market, policy=PricingPolicy()):
    eligible = [q for q in suppliers if q.sku == sku and q.available and q.authorized and q.warranty_ok
                and q.cost.is_finite() and q.shipping.is_finite() and q.cost > 0 and q.shipping >= 0]
    competitors = [m.price for m in market if m.sku == sku and m.verified and m.price.is_finite() and m.price > 0]
    if not eligible or not competitors:
        return {"sku": sku, "status": "BLOCKED", "reason": "missing verified supplier or comparable market quote"}
    rate = policy.tax_rate + policy.payment_rate + policy.warranty_reserve_rate
    if any(not x.is_finite() for x in (rate, policy.fixed_cost, policy.minimum_profit, policy.discount_to_market)) or not (0 <= rate < 1) or policy.fixed_cost < 0 or policy.minimum_profit < 0 or not (0 <= policy.discount_to_market < 1):
        return {"sku": sku, "status": "BLOCKED", "reason": "invalid rate policy"}
    supplier = min(eligible, key=lambda q: q.cost + q.shipping)
    market_low = min(competitors)
    minimum = (supplier.cost + supplier.shipping + policy.fixed_cost + policy.minimum_profit) / (1 - rate)
    price = (market_low * (1 - policy.discount_to_market)).quantize(D("0.01"), rounding=ROUND_HALF_UP)
    profit = price * (1 - rate) - supplier.cost - supplier.shipping - policy.fixed_cost
    if price < minimum or profit < policy.minimum_profit:
        return {"sku": sku, "status": "BLOCKED", "reason": "insufficient margin"}
    return {"sku": sku, "status": "CANDIDATE_ONLY", "supplier": supplier.supplier,
            "supplier_total": str(supplier.cost + supplier.shipping), "market_low": str(market_low),
            "suggested_price": str(price), "estimated_profit": str(profit.quantize(D("0.01"))),
            "tier": tier(category, price), "checkout_enabled": False}
