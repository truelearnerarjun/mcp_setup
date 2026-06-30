# mcp_setup
An MCP server for skill analysis, code review, document summarization, and EKS deployment.

## Project
- `mcp-server/` - FastAPI MCP server implementation
- `frontend/` - browser UI for agent chat, tool invocation, and file uploads
- `MCP_POC_PLAN.md` - original project plan
- `MCP_POC_DOCUMENTATION.md` - legacy POC notes
- `MCP_POC_ACTUAL.md` - current implementation summary
- `PROJECT_COMMANDS.md` - commands for local, Docker, Kubernetes, and Git flows
- `RUN_PROJECT.md` - step-by-step runbook for frontend, EKS backend, and redeploys

## Quick start
1. Build and push the Docker image to ECR.
2. Deploy with `kubectl apply -f mcp-server/rbac.yaml`, `kubectl apply -f mcp-server/deployment.yaml`, `kubectl apply -f mcp-server/service.yaml`, and `kubectl apply -f mcp-server/ingress.yaml`.
3. Point `frontend/index.html` at the ALB hostname in `apiBase`.
4. Use `/tools`, `/invoke`, and `/summarize-file` for API testing.

## Documentation
See `RUN_PROJECT.md` for the normal run steps, `MCP_POC_ACTUAL.md` for the current behavior, and `PROJECT_COMMANDS.md` for the full command reference.
