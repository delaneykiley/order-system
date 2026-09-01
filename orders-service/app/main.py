from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import uuid

from app.database import Base, engine, get_db
from app.models import Order
from app.schemas import OrderCreate, OrderRead

from contextlib import asynccontextmanager


# startup hook
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="orders-service", lifespan=lifespan)


# health check
@app.get("/health")
def health():
    return {"status": "ok", "service": "orders-service"}

# tells FastAPI to validate/serialize return using OrderRead schema
# 201 is correct code for resource creation (vs default 200)
@app.post("/orders", response_model=OrderRead, status_code=201)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    order = Order(item=order_in.item, quantity=order_in.quantity)
    db.add(order)       # stages order for insertion
    db.commit()         # executes the INSERT and commits transaction
    db.refresh(order)   # re-queries row from db and updates attributes to match what's actually stored
    return order

@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: uuid.UUID, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)   # gets Order row whose primary key matches order_id
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders", response_model=list[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).all()