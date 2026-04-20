from dataclasses import dataclass
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Payment
from security import rate_limit
from cryptobot_client import create_invoice


# -----------------------------
#   ТАРИФЫ
# -----------------------------

TARIFFS = {
    "day": {"name": "1 день", "amount": 1.49},
    "month": {"name": "30 дней", "amount": 14.99},
    "year": {"name": "365 дней", "amount": 59.99},
    "lifetime": {"name": "Lifetime", "amount": 89.99},
}


# -----------------------------
#   ЗАПРОС БЕЗ Pydantic
# -----------------------------

@dataclass
class CreateInvoiceRequest:
    tg_id: int
    tariff: str


# -----------------------------
#   ОСНОВНАЯ ФУНКЦИЯ СОЗДАНИЯ ИНВОЙСА
# -----------------------------

def create_invoice_logic(req: CreateInvoiceRequest):
    """
    Полностью заменяет FastAPI endpoint.
    Вызывается напрямую из aiogram-хендлера.
    """

    rate_limit(req.tg_id)

    if req.tariff not in TARIFFS:
        raise ValueError("Неверный тариф")

    tariff_data = TARIFFS[req.tariff]

    # Создаём инвойс через CryptoBot API
    invoice = create_invoice(
        amount=tariff_data["amount"],
        description=tariff_data["name"],
        payload=str(req.tg_id)
    )

    # Сохраняем в БД
    db: Session = SessionLocal()
    payment = Payment(
        tg_id=req.tg_id,
        tariff=req.tariff,
        invoice_id=invoice["invoice_id"],
        status="pending"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return invoice
