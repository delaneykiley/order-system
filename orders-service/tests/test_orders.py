from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

import pytest
from app.database import Base, get_db
from app.main import app

from fastapi.testclient import TestClient

# uses a separate test engine and session (why? test isolation, speed, portability)
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# override get_db dependency to avoid creating Postgres session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# create and drop tables around each test
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)  # create fresh tables
    yield
    Base.metadata.drop_all(bind=engine)    # drop tables

# create test client to make fake HTTP requests
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_order():
    response = client.post("/orders", json={"item": "widget", "quantity": 3})
    assert response.status_code == 201
    assert response.json()["item"] == "widget"
    assert response.json()["quantity"] == 3

def test_create_order_rejects_zero_quantity():
    response = client.post("/orders", json={"item": "widget", "quantity": 0})
    assert response.status_code == 422   # unprocessable entity

def test_get_order_not_found():
    response = client.get("/orders/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}

def test_get_order():
    post_response = client.post("/orders", json={"item": "widget", "quantity": 3})
    order_id = post_response.json()["id"]
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    assert get_response.json()["item"] == "widget"
    assert get_response.json()["quantity"] == 3

def test_list_orders():
    client.post("/orders", json={"item": "widget", "quantity": 3})
    client.post("/orders", json={"item": "widget", "quantity": 6})
    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.json()) >= 2

