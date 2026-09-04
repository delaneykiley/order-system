# Order System

A small distributed system demonstrating service-to-service communication patterns:
synchronous REST calls, asynchronous event-driven messaging, idempotency handling,
and cross-service observability.

## Services

| Service | Port | Responsibility |
|---|---|---|
| `orders-service` | 8001 | Accepts orders, owns order lifecycle |
| `inventory-service` | 8002 | Tracks stock, reserves/releases inventory |
| `notification-service` | 8003 | Sends order confirmations (async, event-driven) |

## Architecture

- `orders-service` → `inventory-service`: **synchronous REST** call to check/reserve stock
  at order time: when an order is created, orders-service calls inventory-service to check whether stock is available. If response status code is 200, then the order is committed to the database with status 'confirmed'. Otherwise, the order is committed to the database with status 'failed' (this preserves a record of what was attempted, at the cost of the client needing to check the order's status separately from the HTTP response code). (IMPLEMENTED)
- `orders-service` → `notification-service`: **asynchronous**, via a Redis Streams event
  (`order.confirmed`) — notification-service consumes it independently. (PLANNED)
- Each request carries a correlation ID that's logged across all three services, so a
  single order can be traced end-to-end. (PLANNED)


## Running locally

```bash
docker compose up --build
```

Then check each service is up:

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

## Roadmap

- [x] Week 1 — scaffolding, Docker Compose, health checks
- [x] Week 2 — orders-service core CRUD (Postgres-backed)
- [x] Week 3 — inventory-service + synchronous integration
- [ ] Week 4 — async messaging via Redis Streams + notification-service
- [ ] Week 5 — idempotency keys + retry/circuit-breaker handling
- [ ] Week 6 — structured logging with correlation IDs across services
- [ ] Week 7 — tests, CI (GitHub Actions), deploy
- [ ] Week 8 — polish, docs, buffer
