# Source Directory Structure

This directory contains the main application code organized into the following packages:

## Packages

- **config/** - Application configuration and settings management
- **models/** - Domain models and data structures
- **repositories/** - Data access layer and database interactions
- **services/** - Business logic and domain services
- **clients/** - External service integrations and API clients
- **controller/** - API endpoints and request handling

## Development Guidelines

- Each package should have a clear, single responsibility
- Dependencies should flow in one direction: controller → services → repositories → models
- External integrations should be isolated in the clients package
- Configuration should be centralized in the config package

## Adding New Features

1. Define data models in `models/`
2. Create repository interfaces in `repositories/`
3. Implement business logic in `services/`
4. Add API endpoints in `controller/`
5. Update configuration in `config/` if needed
