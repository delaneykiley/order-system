from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from app.models import OrderStatus


class OrderCreate(BaseModel):
    # Field() attaches validation constraints: min length of 1 for item str and quantity >0
    item: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)

class OrderRead(BaseModel):
    id: uuid.UUID
    item: str
    quantity: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        # allows pydantic to read attributes from SQLAlchemy object instead of just treating it as a dict
        from_attributes = True