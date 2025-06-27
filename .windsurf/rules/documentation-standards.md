---
trigger: model_decision
---

# Documentation Standards – Python + FastAPI Microservice

This document defines how documentation should be maintained in a FastAPI microservice.

## 1. Code-Level Documentation

### Docstrings

- All public functions, classes, and methods must have docstrings.
- Use consistent format (Google-style or reStructuredText).
- Docstrings must describe:
  - Purpose
  - Parameters
  - Return values
  - Exceptions raised

### Inline Comments

- Explain why non-obvious logic is used.
- Do not restate what the code is doing in obvious cases.

## 2. API Documentation

- Use FastAPI’s built-in OpenAPI docs features.
- Define `response_model` for every route.
- Add descriptions and examples to Pydantic models.
- Use tags and `summary` for each route to organize API docs.

## 3. Project-Level Documentation

### README.md

- Must include:
  - Project overview
  - Setup and install instructions
  - How to run the app and tests
  - Environment/config info
  - API documentation links

### Additional Architecture Docs

- Place under `docs/` if needed.
- May include:
  - Architecture overview
  - External dependencies
  - System diagrams (optional)

## 4. Naming and Structure

- Use consistent, descriptive names for files, classes, and functions.
- Organize code according to layer (e.g., controllers, services, models).

## 5. Maintenance

- Keep documentation up to date with any code or interface changes.
- Outdated documentation must be updated or removed.
