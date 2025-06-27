# Repositories Package

## Purpose
This package handles all data access and persistence logic, acting as an abstraction layer between the database and the application.

## What Belongs Here
- Database models
- Database connection management
- CRUD operations
- Database migrations
- Query building
- Transaction management

## What Does NOT Belong Here
- Business logic (use services package)
- API endpoints (use controller package)
- Request/response models (use models package)

## Guidelines
- One repository per domain entity
- Use async/await for all database operations
- Keep queries simple and focused
- Use type hints for better IDE support
- Implement proper error handling

## Example
```python
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()
```
