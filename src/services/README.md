# Services Package

## Purpose
This package contains the core business logic of the application, implementing use cases and orchestrating interactions between different components.

## What Belongs Here
- Business logic implementation
- Domain services
- Use case handlers
- Validation logic
- Transaction management
- Service composition

## What Does NOT Belong Here
- Data access (use repositories package)
- API endpoints (use controller package)
- Request/response models (use models package)

## Guidelines
- One service per domain or feature
- Services should be stateless
- Use dependency injection for dependencies
- Keep methods focused and single-purpose
- Implement proper error handling and logging

## Example
```python
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        # Business logic here
        if await self.user_repo.get_by_email(user_data.email):
            raise ValueError("Email already registered")
        
        hashed_password = hash_password(user_data.password)
        user = await self.user_repo.create(user_data, hashed_password)
        return UserResponse.from_orm(user)
```
