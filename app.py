from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from engine import SupplierQuote, MarketQuote, evaluate, D

app = FastAPI(title="Wero1Gammer PARADIGMA", version="0.1.1-dev")

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

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wero1Gammer | PARADIGMA</title><style>body{margin:0;background:#0b1020;color:#f1f5f9;font-family:system-ui,Arial,sans-serif}main{max-width:980px;margin:auto;padding:64px 22px}h1{font-size:clamp(2rem,6vw,4rem);margin:12px 0}p{color:#b9c7d9;line-height:1.6}.tag{color:#6ee7b7;letter-spacing:.12em;font-weight:700}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-top:35px}.card{padding:26px;border:1px solid #334155;border-radius:18px;background:#172033}.card h2{margin:0 0 10px}.notice{margin-top:32px;padding:18px;border-left:4px solid #fbbf24;background:#222535}a{color:#93c5fd}</style></head><body><main><div class="tag">PARADIGMA • AMBIENTE DE TESTES</div><h1>Wero1Gammer 🎮</h1><p>Computadores gamers, placas de vídeo e periféricos com análise de custo-benefício.</p><section class="grid"><article class="card"><h2>🥉 PRATA</h2><p>Configurações econômicas</p></article><article class="card"><h2>🥈 OURO</h2><p>Equilíbrio entre preço e desempenho</p></article><article class="card"><h2>🥇 PREMIUM</h2><p>Alto desempenho</p></article></section><div class="notice">Vitrine demonstrativa de staging. Sem ofertas verificadas, checkout ou vendas habilitadas.</div><p><a href="/health">Status técnico</a> · <a href="/docs">Documentação da API</a></p></main></body></html>"""

@app.get("/health")
def health():
    return {"service":"wero1gammer","status":"staging","version":"0.1.1-dev","checkout_enabled":False}

@app.post("/api/pricing/evaluate")
def pricing(payload: EvaluationInput):
    try:
        suppliers = [SupplierQuote(q.supplier,q.sku,D(q.cost),D(q.shipping),q.available,q.authorized,q.warranty_ok) for q in payload.suppliers]
        market = [MarketQuote(m.sku,D(m.price),m.verified) for m in payload.market]
    except ValueError:
        raise HTTPException(status_code=422,detail="Invalid monetary value")
    return evaluate(payload.sku,payload.category,suppliers,market)
