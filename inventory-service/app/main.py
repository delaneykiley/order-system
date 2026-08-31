from fastapi import FastAPI

app = FastAPI(title="inventory-service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "inventory-service"}


# TODO (Week 3): stock levels, reserve/release endpoints
