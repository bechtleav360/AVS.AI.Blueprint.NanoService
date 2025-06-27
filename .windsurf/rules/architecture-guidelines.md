---
trigger: always_on
---

# Architecture Rules – Python + FastAPI Microservice

This document defines the architectural rules for building microservices using Python and FastAPI.

## 1. Layered Architecture

- The codebase must follow a layered architecture with the following packages:
  - `config/` – Global configuration, ensure external configuration (see 12 Factor App)
  - `models/` – Internal domain models used within the application.
  - `services/` – Core business logic and orchestration.
  - `controllers/` – API endpoints and DTO handling (FastAPI routers).
  - `repositories/` – Database or persistent storage access.
  - `clients/` – Integrations with external systems or APIs.

## 2. Model and DTO Separation

- Internal domain models and API-facing DTOs must be defined separately.
- DTOs must be located in the `controllers/` layer.
- Mapping between models and DTOs must be explicit and performed at the controller boundary or via dedicated mappers.

## 3. Repository and Client Isolation

- All database interactions must occur through repository classes.
- All external system interactions must occur through client classes.
- Services must depend only on repositories or clients, never on controllers or DTOs.

## 4. Error Handling

- Raise domain-specific exceptions inside services, clients, and repositories.
- Map exceptions to HTTP responses in centralized exception handlers at the controller level.
- Only the controller layer may use FastAPI’s `HTTPException`.

## 5. Async Design

- All I/O-bound code (e.g., DB queries, HTTP calls) must use `async def`.
- Use only async-compatible libraries for I/O (`httpx`, async DB drivers, etc.).
- Avoid blocking operations such as `time.sleep` or synchronous I/O in async code paths.

## 6. Caching

- Caching may be used only when required for performance and must be justified with metrics.
- Cache logic must be encapsulated outside core business logic, using decorators or adapters.

## 7. Logging and Observability

- Log all unexpected or unhandled errors with full context.
- Include a request ID (e.g., `X-Request-ID`) in all logs for traceability.
- Use FastAPI middleware to log HTTP request and response metadata.

## 8. Dependency Injection and Configuration

- Use FastAPI’s `Depends()` to inject services, repositories, and clients.
- All configuration must be environment-driven and managed via `pydantic.BaseSettings`.
- Global mutable state must be avoided unless explicitly managed through DI or factories.
