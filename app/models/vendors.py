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
    # id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    tel_no = Column(String, nullable=False, unique=True)
    avatar = Column(String, nullable=True)
    status = Column(String, nullable=False, default='Completed', comment="Delivery/Return status")
    createdAt = Column(DateTime(timezone=False), server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="vendor")  
    company = relationship("Company", back_populates="vendor") 

