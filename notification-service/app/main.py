from fastapi import FastAPI

app = FastAPI(title="notification-service")


@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}


# TODO (Week 4): consume order-confirmed events from Redis Streams, log "sent" confirmation
