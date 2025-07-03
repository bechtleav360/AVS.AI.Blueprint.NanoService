# AVS.AI.Blueprint.NanoService

## Introduction

This project is a blueprint for building Python microservices using FastAPI, following a clean layered architecture. It provides a standardized structure for developing maintainable, scalable, and testable REST APIs.

By default, it exposes an endpoint `/echo` which accepts any valid JSON object and echoes it back as the result, demonstrating the basic flow through the application layers.

## Architecture Overview

The application follows a strict layered architecture with clear separation of concerns:

```
┌─────────────────┐
│   Controllers   │  ← API endpoints, request/response handling
├─────────────────┤
│    Services     │  ← Business logic and orchestration
├─────────────────┤
│  Repositories   │  ← Data access and persistence
├─────────────────┤
│     Models      │  ← Domain models and data structures
├─────────────────┤
│     Clients     │  ← External service integrations
├─────────────────┤
│     Config      │  ← Application configuration
└─────────────────┘
```

### Key Architectural Principles

- **Separation of Concerns**: Each layer has a specific responsibility
- **Dependency Flow**: Dependencies flow downward (controllers → services → repositories)
- **Async by Design**: All I/O operations use `async/await` for non-blocking execution
- **Environment-Driven Configuration**: All configuration is externalized
- **Clean API Boundaries**: DTOs are used at API boundaries, separate from domain models

## Project Structure

```
src/
├── config/       # Application configuration
├── models/       # Domain models and data structures
├── repositories/ # Data access layer
├── services/     # Business logic
├── clients/      # External service integrations
└── controller/   # API endpoints
```

## Layers

### Controllers

Controllers handle HTTP requests and responses, defining the API endpoints of the service.

- API route definitions
- Request validation
- Response formatting
- Error handling (HTTP-specific)

Example controllers:
- **ActuatorController**: Provides health checks and metrics
- **StartController**: Renders the landing page
- **EchoController**: Demonstrates basic request/response flow

### Services

Services contain the core business logic of the application.

- Business rules implementation
- Orchestration between repositories and clients
- Domain-specific validation
- Transaction management

### Models

Models define the data structures used throughout the application.

- Pydantic models for validation
- Domain entities
- Data Transfer Objects (DTOs)
- Type definitions

### Repositories

Repositories handle data access and persistence.

- Database operations
- Query building
- Data mapping
- Transaction handling

### Clients

Clients integrate with external services and APIs.

- HTTP clients
- Message queue clients
- Third-party service integrations
- Authentication clients

### Configuration

The configuration layer manages application settings.

- Environment variable handling
- Configuration validation
- Feature flags
- Logging configuration

## Getting Started

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Docker and Docker Compose (optional)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AVS.AI.Blueprint.NanoService
   ```

2. Set up the virtual environment and install dependencies:
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   .\.venv\Scripts\activate  # On Windows
   # or
   # source .venv/bin/activate  # On Unix/macOS
   
   # Install dependencies
   uv pip install -e .  # or use pip install -e .
   ```

3. Configure environment variables:
   see below

4. Run the application:
   ```bash
   python -m src.app
   ```

5. Access the application:
   - API Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc
   - Landing Page: http://localhost:8000/

### Docker Development

For containerized development:

```bash
# Build the image
docker build -t avs-ai-nanoservice .

# Run the container
docker run -it --rm -p 8000:8000 -v ${PWD}:/app avs-ai-nanoservice

# For development with auto-reload
docker run -it --rm -p 8000:8000 -v ${PWD}:/app -e ENVIRONMENT=development avs-ai-nanoservice uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Configuration

The service uses a layered configuration approach based on the dynaconf framework:

### Configuration Hierarchy

1. **Base Configuration**: Global and service-specific configurations are defined in JSON files located in the `config/` directory.

2. **Environment Variables**: Any configuration can be overridden using environment variables, which takes precedence over JSON files. This is particularly useful for:
   - Deployment-specific settings in Helm charts
   - Container configurations in Docker Compose files
   - Local development environment customization

### Usage

Access configuration through the `ConfigurationManager`:

```python
from src.config import ConfigurationManager
# or from idac.configurations if use our external libraries

settings = ConfigurationManager()
db_url = settings.get_config("database_url")
```

### Adding New Configuration

1. Add default values to the JSON file `config/config.json`
2. For environment variable overrides, use the format:
   ```
   DYNACONF_SETTING_NAME=value
   ```

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Model Context Protocol (MCP) Support

This service includes support for the Model Context Protocol (MCP), which enables AI assistants to interact with the API programmatically. MCP allows AI models to discover and use your API's capabilities without hard-coding.

### MCP Features

- **Automatic Route Discovery**: AI assistants can discover available endpoints
- **Operation Descriptions**: Detailed descriptions help AI understand endpoint purposes
- **Parameter Documentation**: Clear parameter documentation ensures correct usage
- **Configurable**: MCP support can be enabled/disabled via the `app_mcp` configuration setting

### Excluded Routes

By default, the following route categories are excluded from MCP:

- `actuators`: Health checks and system information
- `info`: Internal system information

### Configuration

MCP support can be enabled or disabled through the `app_mcp` configuration setting in `config.json` or via environment variables:

## Logging

The service implements structured logging with the following features:

- Request ID tracking for correlation
- Log levels configurable via environment variables
- Log rotation for production environments
- Actuator endpoint `/logs` returns the last 300 log lines

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Code style and formatting
- Development setup
- Testing requirements
- Pull request process
- Documentation standards

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.