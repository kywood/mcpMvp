



PG_HOST=localhost OLLAMA_URL=http://localhost:11434/api/chat MCP_URL=http://localhost:8001/mcp uv run uvicorn main:app --reload --port 8000





curl -X POST http://localhost:8000/failure   -H "Content-Type: application/json"   -d '{
    "dag_id": "test_dag",
    "task_id": "test_task",
    "run_id": "manual__2026-09-15T00:00:00",
    "try_number": 1,
    "exception": "ValueError: division by zero in transform step",
    "log_url": "http://localhost:8080/log?x=1",
    "execution_date": "2026-09-15T00:00:00"
  }'