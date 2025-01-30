import enum
from app.db import Base
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.types import Enum  # Import Enum from SQLAlchemy

class MPESAStatus(str, enum.Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    TIMEOUT = 'timeout'

class STK_Push(Base):
    __tablename__ = 'stk_push'
    stk_id = Column(Integer, primary_key=True)
    merchant_request_id = Column(String, nullable=False)
    checkout_request_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    phone = Column(String, nullable=False)
    status = Column(Enum(MPESAStatus), default=MPESAStatus.PENDING, nullable=False)

    result_code = Column(String, nullable=True)
    result_desc = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
