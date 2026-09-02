from app.schemas import ReserveRequest, ItemRead
from fastapi import FastAPI, Depends, HTTPException
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session
from app.models import Item
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="inventory-service", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok", "service": "inventory-service"}

# decrement stock by some quantity if enough is available
@app.post("/inventory/{item}/reserve")
def reserve_inventory(item: str, request: ReserveRequest, db: Session = Depends(get_db)):
    # atomic update to check how many rows changed after request
    result = db.query(Item).filter(
        Item.item == item,
        Item.quantity_available >= request.quantity
    ).update(
        {"quantity_available": Item.quantity_available - request.quantity},
        synchronize_session=False
    )
    db.commit()

    if result == 0:
        raise HTTPException(status_code=409, detail="Cannot reserve item")
    elif result == 1:
        return {"status": "reserved", "item": item, "quantity": request.quantity}

# re-increment stock
@app.post("/inventory/{item}/release")
def release_inventory(item: str, request: ReserveRequest, db: Session = Depends(get_db)):
    result = (db.query(Item).filter(
        Item.item == item
    ).update(
        {"quantity_available": Item.quantity_available + request.quantity},
        synchronize_session=False
    ))
    db.commit()

    if result == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    elif result == 1:
        return {"status": "released", "item": item, "quantity": request.quantity}


@app.get("/inventory/{item}", response_model=ItemRead)
def get_inventory(item: str, db: Session = Depends(get_db)):
    db_item = db.get(Item, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

