from app.db import Base

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

class Payment(Base):
    __tablename__ = 'payments'
    payment_id = Column(String,primary_key=True)
    sale_id = Column(Integer,ForeignKey('sales.id'),nullable=False)
    amount = Column(Integer,nullable=False)
    mode = Column(String,nullable=False)
    transaction_code = Column(String,nullable=False)
    created_at = Column(DateTime,server_default=func.now())

    sales = relationship("Sale", back_populates="payment")