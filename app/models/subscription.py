from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    tier_id = Column(Integer, ForeignKey("tiers.id"))
    transaction_code = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False, default="active") # Status: active, canceled, expired, etc
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="subscription")
    tier = relationship("Tier", back_populates="subscription")
