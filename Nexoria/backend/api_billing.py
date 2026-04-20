from dataclasses import dataclass
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Payment
from security import rate_limit
from cryptobot_client import create_invoice


TARIFFS = {
    "day": {"name": "1 день", "amount": 1.49},
    "month": {"name": "30 дней", "amount": 14.99},
    "year": {"name": "365 дней", "amount": 59.99},
    "lifetime": {"name": "Lifetime", "amount": 89.99},
}


@dataclass
class CreateInvoiceRequest:
    tg_id: int
    tariff: str


def create_invoice_logic(req: CreateInvoiceRequest) -> dict:
    rate_limit(req.tg_id)

    if req.tariff not in TARIFFS:
        raise ValueError("Неверный тариф")

    tariff_data = TARIFFS[req.tariff]

    invoice = create_invoice(
        amount=tariff_data["amount"],
        description=tariff_data["name"],
        payload=str(req.tg_id),
    )

    db: Session = SessionLocal()
    payment = Payment(
        tg_id=req.tg_id,
        tariff=req.tariff,
        invoice_id=str(invoice["invoice_id"]),
        status="pending",
        amount=tariff_data["amount"],
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return invoice
