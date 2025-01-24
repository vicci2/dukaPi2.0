from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.db import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False, index=True)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False, index=True)
    serial_no = Column(String, nullable=False, unique=True)
    product_name = Column(String, nullable=False, unique=True)
    image = Column(String, nullable=True)
    category = Column(String, nullable=True)
    supplier = Column(String, nullable=True)
    desc = Column(Text, nullable=False, comment="Detailed product description")
    quantity = Column(Numeric, nullable=False, comment="Stock quantity available")
    b_p = Column(Numeric, nullable=False, comment="Base price of the product")
    last_updated = Column(DateTime(timezone=False), server_default=func.now())
    date = Column(DateTime(timezone=False), server_default=func.now())

    # Relationships
    vendor = relationship("Vendor", back_populates="product") 
    inventory = relationship("Inventory", back_populates="product")
    company = relationship("Company", back_populates="product")  
