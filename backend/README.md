# EZCTF Backend

Refactored backend using FastAPI, SQLModel, and PostgreSQL.

## Prerequisites

- Python 3.10+
- `uv` (for package management)
- PostgreSQL

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Configure Database:
   The default configuration connects to `postgresql+psycopg://postgres:postgres@localhost/ezctf`.
   You can change this by setting the `DATABASE_URL` environment variable.

3. Run Migrations:
   ```bash
   uv run alembic -c src/conf/alembic.ini upgrade head
   ```

## Running the Server

```bash
uv run uvicorn src.main:app --reload
```

## Project Structure

- `src/conf`: Configuration and Database setup.
- `src/user`: User model and logic.
- `src/team`: Team model and logic.
- `src/task`: Task model and logic.
- `src/message`: Message model and logic.
- `src/common`: Shared utilities.
