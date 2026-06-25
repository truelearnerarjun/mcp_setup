# MCP Server POC

This project demonstrates a simple MCP server that registers tools and exposes them over HTTP.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn server:app --reload --host 0.0.0.0 --port 8000
   ```

## Endpoints

- `GET /` - health check
- `GET /tools` - list registered tools
- `POST /invoke` - invoke a tool

## Example invoke request

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool": "review_python_code", "input": "import os\nprint(\"hello\")"}'
```
