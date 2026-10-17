from fastapi import FastAPI
from pydantic import BaseModel, Field
from engine import SupplierQuote, MarketQuote, evaluate, D

app = FastAPI(title="Wero1Gammer PARADIGMA", version="0.1.0-dev")

class QuoteInput(BaseModel):
    supplier: str
    sku: str
    cost: str
    shipping: str
    available: bool
    authorized: bool
    warranty_ok: bool

class MarketInput(BaseModel):
    sku: str
    price: str
    verified: bool

class EvaluationInput(BaseModel):
    sku: str = Field(min_length=1)
    category: str = Field(min_length=1)
    suppliers: list[QuoteInput] = Field(max_length=100)
    market: list[MarketInput] = Field(max_length=100)

@app.get("/health")
def health():
    return {"service": "wero1gammer", "status": "staging", "version": "0.1.0-dev", "checkout_enabled": False}

@app.post("/api/pricing/evaluate")
def pricing(payload: EvaluationInput):
    from fastapi import HTTPException
    try:
        suppliers = [SupplierQuote(q.supplier, q.sku, D(q.cost), D(q.shipping), q.available, q.authorized, q.warranty_ok) for q in payload.suppliers]
        market = [MarketQuote(m.sku, D(m.price), m.verified) for m in payload.market]
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid monetary value")
    return evaluate(payload.sku, payload.category, suppliers, market)
