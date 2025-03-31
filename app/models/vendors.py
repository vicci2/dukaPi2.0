# This file is used to scalulpt the Sales Model/Table in the system Database:

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db import Base

# The Sales Model:
class Vendor(Base):
    # attaching a prefered tablename:
    __tablename__='vendors'
    # Column defination:
    id = Column(Integer, primary_key=True, index=True) 
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    tel_no = Column(String, nullable=False, unique=True)
    last_update = Column(DateTime(timezone=False), server_default=func.now()) 
    createdAt = Column(DateTime(timezone=False), server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="vendor")  
    company = relationship("Company", back_populates="vendor") 

