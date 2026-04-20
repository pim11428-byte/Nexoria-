from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, index=True, nullable=False)
    tariff = Column(String, nullable=False)
    invoice_id = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="pending", nullable=False)
    amount = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
