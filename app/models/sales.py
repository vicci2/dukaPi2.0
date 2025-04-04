# This file is used to scalulpt the Sales Model/Table in the system Database:

from enum import Enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

# We need to make sure that this model also meets our set specs in the db.base file Base class..... si:
from app.db import Base


class SaleStatus(str, Enum):
    COMPLETED = "Completed"
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    
# The Sales Model:
class Sale(Base):
    # attaching a prefered tablename:
    __tablename__='sales'
    # Column defination:
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id", ondelete="SET NULL",), nullable=False, index=True)
    quantity = Column(Numeric(10, 2), nullable=False, comment="Quantity sold")
    base_price = Column(Numeric(10, 2), nullable=False, comment="Base price during sale")
    selling_price = Column(Numeric(10, 2), nullable=False, comment="Selling price during sale")
    last_updated = Column(DateTime(timezone=False), server_default=func.now())
    sale_date = Column(DateTime(timezone=False), server_default=func.now())
    status = Column(String, nullable=False, default='Completed', 
    comment="Sale status")
    # status = Column(String, nullable=False, default=SaleStatus.PENDING)

    # Relationships
    inventory = relationship("Inventory", back_populates="sales") 
    company = relationship("Company", back_populates="sales")  
    payment = relationship("Payment", back_populates="sales")
 

