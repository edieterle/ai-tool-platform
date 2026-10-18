start server: uv run mcp dev server.py
test server: uv run pytest -v

format imports: uv run ruff check --select I --fix .
format code: uv run ruff format .

start containers: docker compose up -d
stop containers: docker compose down
remove Compose-managed named volumes: docker compose down -v
