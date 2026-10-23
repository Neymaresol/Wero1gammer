# Wero1Gammer PARADIGMA — 0.1.0-dev

MVP de precificacao de computadores gamer PRATA/OURO/PREMIUM, placas e perifericos.

## Executar

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
python -m unittest discover -s tests -v
```

`GET /health` e `POST /api/pricing/evaluate`.

## Double Check

- Retorna somente candidatos de precificacao, nunca pedidos aprovados.
- Checkout, compras, transferencias e publicacao automatica desativados.
- Cotacoes sao fornecidas por quem chama a API; ainda nao ha integracao B2B autenticada.
- Taxas e reservas sao premissas ilustrativas, nao valores fiscais validados.
- Nunca enviar credenciais ou dados de pagamento para esta API.
- Nenhuma alteracao em producao PARADIGMA.
