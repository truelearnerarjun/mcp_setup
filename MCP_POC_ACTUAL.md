# MCP POC Actual Implementation

## Purpose
This project is a skills-focused MCP server with a browser UI and Kubernetes deployment manifests.

## Current Behavior

### Agent chat
- Accepts only prompts that match the registered MCP skills
- Supports Python code review, PPT creation, document summarization, AWS cost analysis, SQL generation, architecture diagrams, frontend review, DevOps review, quality review, backend review, and Bedrock text generation
- Rejects unrelated prompts such as general chat, weather, or random Q&A

### File upload and summarization
- Lets the user upload `.txt`, `.pdf`, or `.docx` files from the Agent Chat panel
- Extracts full text from the file with a large configurable limit
- Summarizes the main content rather than only the first paragraph
- Filters contact-style and metadata-style lines when building the summary

### Backend tools
- `review_python_code`
- `create_ppt`
- `summarize_document`
- `aws_cost_analyzer`
- `sql_generator`
- `architecture_diagram_generator`
- `frontend_developer`
- `devops_engineer`
- `quality_engineer`
- `backend_developer`
- `bedrock_text_generator`
- `assistant_agent`

## Runtime Paths

### Local development
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

### Kubernetes
- Backend deployment: `mcp-server/deployment.yaml`
- Internal service: `mcp-server/service.yaml`
- ALB ingress: `mcp-server/ingress.yaml`
- Bedrock role binding: `mcp-server/rbac.yaml`

## Operational Notes

- The frontend contains a commented local API base and an ALB placeholder so it can be toggled during development.
- The summary endpoint uses a threadpool for extraction and summarization work.
- The document readers support `.txt`, `.pdf`, and `.docx`.

## What Is Not In Scope

- OCR for scanned PDFs
- PPT/PPTX text extraction
- Full LLM-generated summaries for every file type

Those can be added later if needed.
