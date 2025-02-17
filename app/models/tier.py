from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db import Base

# Association table for Many-to-Many relationship
tier_features = Table(
    "tier_features",
    Base.metadata,
    Column("tier_id", Integer, ForeignKey("tiers.id"), primary_key=True),
    Column("feature_id", Integer, ForeignKey("features.id"), primary_key=True)
)

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    # Many-to-Many Relationship with Tiers
    tiers = relationship("Tier", secondary=tier_features, back_populates="features")


class Tier(Base):
    __tablename__ = "tiers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  #monthly or yearly

    # Many-to-Many Relationship with Features
    features = relationship("Feature", secondary=tier_features, back_populates="tiers")

    # One-to-Many Relationship with Subscription
    subscription = relationship("Subscription", back_populates="tier")

    # # Establish reverse relationship on the Feature model
    # Feature.tiers = relationship("Tier", secondary=tier_features, back_populates="features")
