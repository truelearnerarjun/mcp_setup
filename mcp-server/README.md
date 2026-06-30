# MCP Server POC

FastAPI-based MCP server for skills-focused agent chat, tool discovery, and document summarization.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /` - health check
- `GET /tools` - list registered tools
- `POST /invoke` - invoke a registered tool
- `POST /summarize-file` - upload and summarize `.txt`, `.pdf`, or `.docx`

## Notes

- `assistant_agent` only responds to registered MCP skills.
- File uploads extract text before summarization.
- The backend can run with Bedrock enabled or use local fallback responses.
