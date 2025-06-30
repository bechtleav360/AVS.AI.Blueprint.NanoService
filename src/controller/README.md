# Controller Package

## Purpose
This package contains all API endpoints and request/response handling logic, serving as the entry point for HTTP requests.

## What Belongs Here
- API route definitions
- Request validation
- Response formatting
- Authentication/authorization
- Dependency injection for services
- Error handling

## What Does NOT Belong Here
- Business logic (use services package)
- Data access (use repositories package)
- Data models (use models package)

## Guidelines
- Group related endpoints in separate router files
- Use FastAPI's dependency injection
- Keep controllers thin - delegate business logic to services
- Document all endpoints with OpenAPI
- Implement proper error handling

## Example
```python
router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Create a new user."""
    try:
        return await user_service.register_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get user by ID."""
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```
