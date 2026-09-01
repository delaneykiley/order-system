from pydantic import BaseModel, Field, ConfigDict
import uuid
from datetime import datetime
from app.models import OrderStatus


class OrderCreate(BaseModel):
    # Field() attaches validation constraints: min length of 1 for item str and quantity >0
    item: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)

class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    item: str
    quantity: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

