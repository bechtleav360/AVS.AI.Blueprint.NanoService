# Clients Package

## Purpose
This package contains all external service integrations and API clients used by the application.

## What Belongs Here
- HTTP clients for external APIs
- Message queue clients
- Third-party service integrations
- Authentication clients
- Caching clients
- Client configuration

## What Does NOT Belong Here
- Business logic (use services package)
- Database access (use repositories package)
- Application configuration (use config package)

## Guidelines
- One client per external service
- Use async/await for all I/O operations
- Implement retry logic for transient failures
- Add proper error handling and logging
- Use environment variables for configuration

## Example
```python
class PaymentClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = AsyncClient(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"}
        )

    async def process_payment(self, payment_data: dict) -> dict:
        try:
            response = await self.client.post("/payments", json=payment_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Payment processing failed: {e}")
            raise
```
