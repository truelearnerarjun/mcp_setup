# mcp_setup
Making an MCP server for skill analysis and connecting with EKS.

## Project
- `mcp-server/` — FastAPI MCP server implementation
- `frontend/` — minimal browser UI for tool discovery and invocation
- `MCP_POC_PLAN.md` — project plan
- `MCP_POC_DOCUMENTATION.md` — deployment and usage documentation

## Quick start
1. Build and push the Docker image to ECR.
2. Deploy with `kubectl apply -f mcp-server/deployment.yaml` and `kubectl apply -f mcp-server/service.yaml`.
3. Open `frontend/index.html` or use the `/tools` and `/invoke` endpoints directly.

## Documentation
See `MCP_POC_DOCUMENTATION.md` for the full POC process.
