from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid

from app.database import Base, engine, get_db
from app.models import Order
from app.schemas import OrderCreate, OrderRead

app = FastAPI(title="orders-service")

# startup hook
@app.on_event("startup")
def on_startup():
    # checks the db for every model class that inherits from Base and
    # creates any table that doesn't exist yet based on the model's column definitions
    Base.metadata.create_all(bind=engine)

# health check
@app.get("/health")
def health():
    return {"status": "ok", "service": "orders-service"}

# tells FastAPI to validate/serialize return using OrderRead schema
# 201 is correct code for resource creation (vs default 201)
@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    order = Order(item=order_in.item, quantity=order_in.quantity)
    db.add(order)       # stages order for insertion
    db.commit()         # executes the INSERT and commits transaction
    db.refresh(order)   # re-queries row from db and updates attributes to match what's actually stored

    return order