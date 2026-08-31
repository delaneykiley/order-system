from fastapi import FastAPI

app = FastAPI(title="orders-service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "orders-service"}


# TODO (Week 2): order creation endpoint, order model, Postgres persistence
