from sqlalchemy import Column, Integer, String, Float
from app.db import Base
from sqlalchemy.orm import relationship

class Tier(Base):
    __tablename__ = "tiers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    subscription = relationship("Subscription", back_populates="tier")