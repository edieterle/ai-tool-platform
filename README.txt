start server: uv run mcp dev server.py
test server: uv run pytest -v

format imports: uv run ruff check --select I --fix .
format code: uv run ruff format .

start Docker container: docker compose up -d
enable pgvector (only do this once): docker compose exec postgres psql -U appuser -d appdb -c "CREATE EXTENSION IF NOT EXISTS vector;"
