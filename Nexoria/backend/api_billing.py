from fastapi import APIRouter
from pydantic import BaseModel
from cryptobot_client import create_invoice
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Payment
from security import rate_limit

router = APIRouter()


class CreateInvoiceRequest(BaseModel):
    tg_id: int
    tariff: str


TARIFFS = {
    "day": {"name": "1 день", "amount": 1.49},
    "month": {"name": "30 дней", "amount": 14.99},
    "year": {"name": "365 дней", "amount": 59.99},
    "lifetime": {"name": "Lifetime", "amount": 89.99},
}


@router.post("/create_invoice")
def create_invoice_endpoint(req: CreateInvoiceRequest):
    # защита от флуда
    rate_limit(str(req.tg_id))

    tariff = TARIFFS[req.tariff]

    invoice = create_invoice(
        amount=tariff["amount"],
        asset="USDT",
        description=tariff["name"],
        payload={"tg_id": req.tg_id, "tariff": req.tariff}
    )

    db: Session = SessionLocal()

    payment = Payment(
        tg_id=req.tg_id,
        tariff=req.tariff,
        amount=tariff["amount"],
        asset="USDT",
        invoice_id=invoice["invoice_id"],
        pay_url=invoice["pay_url"],
        status="pending"
    )

    db.add(payment)
    db.commit()

    return {
        "tariff_name": tariff["name"],
        "amount": tariff["amount"],
        "asset": "USDT",
        "pay_url": invoice["pay_url"],
    }

