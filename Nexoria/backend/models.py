from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, index=True)
    status = Column(String)  # inactive / active / lifetime
    expires_at = Column(DateTime, nullable=True)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, index=True)
    tariff = Column(String)
    amount = Column(Float)
    asset = Column(String)
    invoice_id = Column(String)
    pay_url = Column(String)
    status = Column(String, default="pending")  # pending / paid
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
