---
trigger: model_decision
description: The generated code throws errors or catches exceptions
---

# Error Handling Rules

## Error Classes

1. Use BaseAPIError as the base class for all API errors
2. For client errors (4xx), use these subclasses:
   - BadRequestError (400): Invalid request format or parameters
   - UnauthorizedError (401): Authentication required or failed
   - ForbiddenError (403): Insufficient permissions
   - NotFoundError (404): Resource not found
   - ConflictError (409): Resource conflict
   - ValidationError (422): Request validation failed
3. For server errors (5xx), use:
   - InternalServerError (500): Generic server error
   - NotImplementedError (501): Functionality not implemented
   - ServiceUnavailableError (503): Service unavailable

## Error Response Format

All errors must return:

```json
{
  "code": "error_code",
  "message": "Human-readable message",
  "details": {
    "key": "Additional context"
  }
}
```

## Best Practices

- Be specific with error types
- Provide actionable error messages
- Include relevant context in details
- Log errors before converting to API errors
- Document expected errors in API documentation (see documentation-standards.md)
