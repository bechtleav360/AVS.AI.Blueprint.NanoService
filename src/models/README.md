# Models Package

## Purpose
This package contains all domain models and data structures used throughout the application.

## What Belongs Here
- Pydantic models for request/response validation
- Domain entities
- Data transfer objects (DTOs)
- Type definitions
- Enums and constants

## What Does NOT Belong Here
- Database models (use repositories package)
- Business logic (use services package)
- API endpoints (use controller package)

## Naming Conventions
- Use `*Request` suffix for input models
- Use `*Response` suffix for output models
- Use `*Base` for base models with common fields
- Keep models focused and single-purpose

## Example
```python
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
```
