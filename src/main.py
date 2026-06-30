from fastapi import FastAPI

from src.presentation.balance_router import balance

app = FastAPI(
    title="Top Bank API",
    version="1.0.0",
)

app.include_router(balance)

@app.get("/health", tags=["System"])
def health_check() -> dict[str, str]:
    """
    Endpoint de verificação de saúde da API.
    Utilizado por ferramentas de orquestração e monitoramento.
    """
    return {"status": "ok"}