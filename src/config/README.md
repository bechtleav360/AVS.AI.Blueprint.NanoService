# Configuration Package

## Purpose
This package is responsible for managing all application configuration and settings.

## What Belongs Here
- Environment variable handling
- Configuration validation
- Default settings
- Configuration models using Pydantic
- Logging configuration
- Feature flags

## What Does NOT Belong Here
- Business logic
- API endpoints
- Database models
- External service clients

## Usage
```python
from src.config.config import ConfigurationManager

settings = ConfigurationManager()
db_url = settings.get_config("database_url")
```

## Adding New Configuration
1. Add new environment variables to `.env`
2. Update `config.json` to include new settings
3. Add validation rules if needed
