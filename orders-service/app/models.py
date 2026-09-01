from datetime import datetime, timezone
import uuid
import enum

import sqlalchemy

from app.database import Base

from sqlalchemy import Column, String, Integer, DateTime, Enum

from sqlalchemy.dialects import postgresql


class OrderStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"

class Order(Base):
    __tablename__ = "orders"
    id = Column(postgresql.UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    item = Column(String)
    quantity = Column(Integer)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))



