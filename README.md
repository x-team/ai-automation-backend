# AI Automation Back-end

## Overview

This project is intended to be a collaborative place for AI developers to create and test new applications. The project is built using FastAPI, a modern Python web framework that is both fast and easy to use.

## Table of Contents

-   [Requirements](#requirements)
-   [Installation](#installation)
    -   [Poetry Setup](#poetry-setup)
    -   [Pre-commit Hooks](#pre-commit-hooks)
    -   [Configuration](#configuration)
-   [Project Structure](#project-structure)
-   [Usage](#usage)
    -   [Docker Deployment](#docker-deployment)
    -   [Running the Application Without Docker](#running-the-application-without-docker)
    -   [Accessing Documentation](#accessing-documentation)
    -   [Creating an Account](#creating-an-account)
-   [Database Migrations](#database-migrations)
    -   [Applying Migrations](#applying-migrations)
    -   [Reverting Migrations](#reverting-migrations)
    -   [Generating Migrations](#generating-migrations)
-   [Running Tests](#running-tests)

## Requirements

To run this project, ensure you have the following installed:

-   Python 3.12
-   [Poetry](https://python-poetry.org/docs/#installation)
-   [Alembic](https://alembic.sqlalchemy.org/en/latest/)
-   [Docker](https://docs.docker.com/get-docker/)

## Installation

### Poetry Setup

This project utilizes [Poetry](https://python-poetry.org/) for dependency management, simplifying package management and ensuring consistent environments.

1. **Install Poetry**: Follow the [official installation guide](https://python-poetry.org/docs/#installation).

2. **Install Project Dependencies**:

    ```bash
    poetry install
    ```

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:

```bash
pre-commit install
```

The pre-commit configuration (`.pre-commit-config.yaml`) includes:

-   **Black**: Code formatter
-   **Mypy**: Type checker
-   **Ruff**: Linter for spotting potential bugs

Learn more about pre-commit [here](https://pre-commit.com/).

### Configuration

Configure the application using environment variables. Create a `.env` file in the root directory and define variables. For instance:

```bash
OPENAI_API_KEY=
```

For more details, refer to the [Pydantic BaseSettings documentation](https://pydantic-docs.helpmanual.io/usage/settings/).

## Project Structure

```bash
apps
├── tests                  # Test suite
├── api                    # API endpoints
│   ├── v1                 # Version 1 of the API
│   │   └── routers        # API route handlers
│   ├── main.py            # FastAPI application setup
│   ├── lifespan.py        # Application lifecycle management
│   └── router.py          # Main router configuration
├── core                   # Core application components
│   ├── config             # Configuration settings
│   │   └── settings.py    # Application settings
│   ├── utils              # Utility functions
│   ├── docs               # API documentation assets
│   ├── infra              # Infrastructure components
│   │   └── sql_alchemy    # Database configuration
│   │       ├── base.py    # SQLAlchemy base configuration
│   │       ├── dependencies.py # Database dependencies
│   │       ├── meta.py    # Metadata configuration
│   │       ├── migrations # Database migrations
│   │       └── db_utils.py # Database utilities
│   └── middleware          # Middleware providers
├── modules                # Business logic modules
│   ├── shared             # Shared module
│   │   ├── controllers    # Business logic controllers
│   │   ├── infra          # Module infrastructure
│   │   │   └── sql_alchemy
│   │   │       ├── models       # Data models
│   │   │       └── repositories # Data repositories
│   │   ├── schemas        # Data schemas
│   │   ├── repository_interfaces # Repository interfaces
│   │   └── services       # Business services
│   ├── module        # Module
│   │   ├── controllers    # Module controllers
│   │   ├── infra          # Module infrastructure
│   │   ├── schemas        # Module schemas
│   │   └── services       # Module services
│   └── ...                # Additional application modules
└── __main__.py            # Application entry point
```

## Usage

### Docker Deployment

For development with autoreload and exposed ports, use:

```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This setup exposes the web application on port 8000, mounts the current directory, and enables autoreload.

**Note**: Rebuild the image after modifying `poetry.lock` or `pyproject.toml`:

### Running the Application Without Docker

Start the application using Poetry:

```bash
poetry run python -m apps
```

This command launches the server on the configured host.

### Accessing Documentation

Once the server is running, access the Swagger documentation at `/api/v1/docs`.

## Database Migrations

Manage database migrations using Alembic.

### Applying Migrations

To apply migrations:

```bash
# Apply all migrations up to a specific revision.
alembic upgrade "<revision_id>"

# Apply all pending migrations.
alembic upgrade head
```

### Reverting Migrations

To revert migrations:

```bash
# Revert to a specific revision.
alembic downgrade <revision_id>

# Revert all migrations.
alembic downgrade base
```

### Generating Migrations

To generate new migrations:

```bash
# Automatic change detection.
alembic revision --autogenerate

# Generate an empty migration file.
alembic revision
```

## Running Tests

To run tests:

1. **Using Docker**:

    ```bash
    docker-compose run --build --rm api pytest -vv .
    docker-compose down
    ```

2. **Locally**:

    - Start a PostgreSQL database (e.g., using Docker):

        ```bash
        docker run -p "5432:5432" -e "POSTGRES_USER=postgres" -e "POSTGRES_DB=postgres" -e "POSTGRES_PASSWORD=password" postgres
        ```
