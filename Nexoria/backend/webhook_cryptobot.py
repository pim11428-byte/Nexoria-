from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Payment
from domain_subscriptions import activate_subscription

router = APIRouter()


@router.post("/callback")
async def cryptobot_callback(request: Request):
    data = await request.json()

    if "update_type" not in data:
        return {"ok": True}

    if data["update_type"] != "invoice_paid":
        return {"ok": True}

    payload = data["payload"]
    tg_id = int(payload["tg_id"])
    tariff = payload["tariff"]

    db: Session = SessionLocal()

    # обновляем платеж
    payment = db.query(Payment).filter(Payment.invoice_id == payload["invoice_id"]).first()
    if payment:
        payment.status = "paid"
        db.commit()

    # активируем подписку
    activate_subscription(db, tg_id, tariff)

    return {"ok": True}
