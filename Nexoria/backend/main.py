from fastapi import FastAPI
from api_osint import router as osint_router
from api_billing import router as billing_router

app = FastAPI(title="NEXORIA Backend")

app.include_router(osint_router, prefix="/api/osint", tags=["osint"])
app.include_router(billing_router, prefix="/api/billing", tags=["billing"])

@app.get("/api/subscriptions/status")
def subscription_status(tg_id: int):
    # временная заглушка
    return {"status": "inactive", "expires_at": None}
    from database import Base, engine

Base.metadata.create_all(bind=engine)
