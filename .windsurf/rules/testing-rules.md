---
trigger: model_decision
---

# Testing Rules – Python + FastAPI Microservice

This document defines rules for testing FastAPI microservices. Only unit and system tests are required.

## 1. Testing Scope

- Two test types are required:
  - **Unit Tests** – Test individual functions or classes in isolation.
  - **System Tests** – Test the API via HTTP requests with all backend systems mocked.

## 2. Unit Tests

- Test single components in isolation with full mocking of external dependencies.
- Use `pytest`, `pytest-mock`, or `unittest.mock` for mocking.
- Place unit tests under `tests/unit/`, mirroring the project structure.
- Avoid side effects, I/O operations, or real service calls.

## 3. System Tests

- Simulate complete HTTP flows using FastAPI’s `TestClient` or `httpx.AsyncClient`.
- All backend systems (DB, queues, external APIs) must be mocked.
- Place system tests in `tests/system/`.
- System tests must cover:
  - Input validation
  - Status code correctness
  - Side effect behavior (mocked)
  - Data contract integrity

## 4. Test Structure and Naming

- Test files must be named `test_<module>.py`.
- Each test function must be named clearly using the format: `test_<functionality>_<expected_behavior>()`.

## 5. Fixtures and Isolation

- Use `pytest` fixtures for shared setup and teardown.
- Each test must be isolated and able to run independently.
- Avoid using shared mutable state across tests.

## 6. Performance and Determinism

- Tests must be fast and deterministic.
- Do not include real network calls, time-based logic, or filesystem access in unit/system tests.

## 7. CI Integration

- All tests must run on every push and pull request in CI.
- CI must fail if any test fails.
- Code coverage must be reported and monitored.

## 8. Required Tools

- `pytest`
- `pytest-asyncio`
- `httpx` or `TestClient` from FastAPI
- `unittest.mock` or `pytest-mock`
- `coverage.py` for coverage tracking
