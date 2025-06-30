---
trigger: model_decision
description: The generated code throws errors or catches exceptions
---

# Error Handling Rules

## Error Classes
1. Use [BaseAPIError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:23:0-38:49) as the base class for all API errors
2. For client errors (4xx), use these subclasses:
   - [BadRequestError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:62:0-65:50) (400): Invalid request format or parameters
   - [UnauthorizedError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:73:0-78:70) (401): Authentication required or failed
   - [ForbiddenError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:31:0-36:61) (403): Insufficient permissions
   - [NotFoundError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:82:0-86:57) (404): Resource not found
   - [ConflictError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:97:0-102:64) (409): Resource conflict
   - [ValidationError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:96:0-100:55) (422): Request validation failed
3. For server errors (5xx), use:
   - [InternalServerError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:122:0-126:44) (500): Generic server error
   - [NotImplementedError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:129:0-134:62) (501): Functionality not implemented
   - [ServiceUnavailableError](cci:2://file:///c:/Users/pajom/Git/avs/AVS.AI.Blueprint.NanoService/src/models/errors.py:137:0-142:52) (503): Service unavailable

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


## Best Practices
* Be specific with error types
* Provide actionable error messages
* Include relevant context in details
* Log errors before converting to API errors
* Document expected errors in API documentation (see documentation-standards.md)