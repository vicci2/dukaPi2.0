from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    socials = Column(String, nullable=True)
    # branches = Column(String, nullable=True)

    user = relationship("User", back_populates="company")
    subscription = relationship("Subscription", back_populates="company")
    product = relationship("Product", back_populates="company") 
    inventory = relationship("Inventory", back_populates="company") 
    sales = relationship("Sale", back_populates="company") 
    vendor = relationship("Vendor", back_populates="company") 