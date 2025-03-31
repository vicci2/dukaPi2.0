from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    tier_id = Column(Integer, ForeignKey("tiers.id"))
    transaction_code = Column(String, unique=True,)
    status = Column(String, nullable=False, default="pending")
    # start_date = Column(DateTime(timezone=False), server_default=func.now()) 
    # expiry_date = Column(DateTime(timezone=False), server_default=func.now()) 
    last_update = Column(DateTime(timezone=False), server_default=func.now()) 
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="subscription")
    tier = relationship("Tier", back_populates="subscription")
