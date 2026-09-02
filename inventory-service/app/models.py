from app.database import Base

from sqlalchemy import Column, String, Integer, CheckConstraint, DateTime

from datetime import datetime, timezone


class Item(Base):
    __tablename__ = "items"
    # independently enforces >=0 restraint on item quantity at database level
    __table_args__ = (
        CheckConstraint("quantity_available >= 0", name="quantity_non_negative"),
    )

    item = Column(String, primary_key=True)
    quantity_available = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

