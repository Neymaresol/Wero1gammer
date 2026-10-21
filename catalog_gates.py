"""Offline catalog eligibility gate: never authorizes a purchase or publishes a listing."""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

TIERS = {"prata", "ouro", "premium"}
CATEGORIES = {"computador", "placa_video", "processador", "memoria", "ssd", "monitor", "periferico"}

@dataclass(frozen=True)
class CatalogCandidate:
    sku: str
    tier: str
    category: str
    supplier_authorized: bool
    stock_confirmed: bool
    warranty_confirmed: bool
    market_price_verified: bool
    supplier_total_brl: str
    proposed_price_brl: str

def validate(candidate: CatalogCandidate) -> dict:
    reasons = []
    if not candidate.sku.strip():
        reasons.append("missing_sku")
    if candidate.tier not in TIERS:
        reasons.append("invalid_tier")
    if candidate.category not in CATEGORIES:
        reasons.append("invalid_category")
    if not candidate.supplier_authorized:
        reasons.append("supplier_not_authorized")
    if not candidate.stock_confirmed:
        reasons.append("stock_not_confirmed")
    if not candidate.warranty_confirmed:
        reasons.append("warranty_not_confirmed")
    if not candidate.market_price_verified:
        reasons.append("market_price_not_verified")
    try:
        cost = Decimal(candidate.supplier_total_brl)
        price = Decimal(candidate.proposed_price_brl)
        if not cost.is_finite() or not price.is_finite() or cost <= 0 or price <= cost:
            reasons.append("invalid_margin")
    except (InvalidOperation, ValueError):
        reasons.append("invalid_money")
    return {"sku": candidate.sku, "eligible_for_review": not reasons,
            "reasons": reasons, "publish_enabled": False, "checkout_enabled": False}
