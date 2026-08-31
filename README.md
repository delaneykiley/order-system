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

## Architecture (planned)

- `orders-service` → `inventory-service`: **synchronous REST** call to check/reserve stock
  at order time.
- `orders-service` → `notification-service`: **asynchronous**, via a Redis Streams event
  (`order.confirmed`) — notification-service consumes it independently.
- Each request carries a correlation ID that's logged across all three services, so a
  single order can be traced end-to-end.

_This section will be filled in with real design decisions and tradeoffs as the system
is built out — see the roadmap below._

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
- [ ] Week 2 — orders-service core CRUD (Postgres-backed)
- [ ] Week 3 — inventory-service + synchronous integration
- [ ] Week 4 — async messaging via Redis Streams + notification-service
- [ ] Week 5 — idempotency keys + retry/circuit-breaker handling
- [ ] Week 6 — structured logging with correlation IDs across services
- [ ] Week 7 — tests, CI (GitHub Actions), deploy
- [ ] Week 8 — polish, docs, buffer
