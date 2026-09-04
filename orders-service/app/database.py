import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# create engine with ping flag (to automatically test and repair stale database connections before use)
db_url = os.environ.get("DATABASE_URL", "postgresql://app:app@localhost:5432/orders")

engine = create_engine(db_url, pool_pre_ping=True)

# create session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# create declarative base
Base = declarative_base()

# dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()