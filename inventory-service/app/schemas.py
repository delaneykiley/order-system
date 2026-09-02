from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ReserveRequest(BaseModel):
    quantity: int = Field(..., gt=0)

class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    item:str
    quantity_available:int
    created_at: datetime
    updated_at: datetime

