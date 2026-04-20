from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User, Subscription, Payment


TARIFF_DURATIONS = {
    "day": timedelta(days=1),
    "month": timedelta(days=30),
    "year": timedelta(days=365),
    "lifetime": None
}


def get_or_create_user(db: Session, tg_id: int):
    user = db.query(User).filter(User.tg_id == tg_id).first()
    if not user:
        user = User(tg_id=tg_id)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def activate_subscription(db: Session, tg_id: int, tariff: str):
    user = get_or_create_user(db, tg_id)

    sub = db.query(Subscription).filter(Subscription.tg_id == tg_id).first()

    if tariff == "lifetime":
        if not sub:
            sub = Subscription(
                tg_id=tg_id,
                status="lifetime",
                expires_at=None
            )
            db.add(sub)
        else:
            sub.status = "lifetime"
            sub.expires_at = None

        db.commit()
        return sub

    duration = TARIFF_DURATIONS[tariff]
    now = datetime.utcnow()

    if not sub:
        sub = Subscription(
            tg_id=tg_id,
            status="active",
            expires_at=now + duration
        )
        db.add(sub)
    else:
        if sub.status == "active" and sub.expires_at:
            sub.expires_at += duration
        else:
            sub.status = "active"
            sub.expires_at = now + duration

    db.commit()
    return sub


def get_subscription_status(db: Session, tg_id: int):
    sub = db.query(Subscription).filter(Subscription.tg_id == tg_id).first()

    if not sub:
        return {"status": "inactive", "expires_at": None}

    if sub.status == "lifetime":
        return {"status": "lifetime", "expires_at": None}

    if sub.expires_at and sub.expires_at < datetime.utcnow():
        return {"status": "inactive", "expires_at": sub.expires_at}

    return {"status": "active", "expires_at": sub.expires_at}
