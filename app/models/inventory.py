# This file is used to scalulpt the Products Model/Table in the system Database:
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

# We need to make sure that this model also meets our set specs in the db.base file Base class..... si:
from app.db import Base

# The Products Model:
class Inventory(Base):
    # attaching a prefered tablename:     
    __tablename__ = 'inventory'
    # Column defination:
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False, index=True)
    quantity = Column(Numeric, nullable=False, comment="Stock quantity available")
    base_price = Column(Numeric, nullable=False, comment="Base price of the product")
    selling_price = Column(Numeric, nullable=False, comment="Selling price of the product")
    serial_no = Column(String, nullable=False, unique=True)  
    date = Column(DateTime(timezone=False), server_default=func.now())
    last_updated = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())

    # Relationships
    sales = relationship("Sale", back_populates="inventory")
    product = relationship("Product", back_populates="inventory") 
    company = relationship("Company", back_populates="inventory")   
    