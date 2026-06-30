# Process Documentation

This document describes the process that has been followed while building and deploying the MCP codebase.

## 1. Project Setup and Planning

- Defined the project goal: build a small MCP server POC with tool discovery, invocation, and a browser UI.
- Created project structure with `frontend/`, `mcp-server/`, and root documentation files.
- Recorded planning and architecture intent in `MCP_POC_PLAN.md` and `MCP_POC_DOCUMENTATION.md`.

## 2. Backend Implementation

- Implemented the FastAPI server in `mcp-server/server.py`.
- Added CORS middleware to allow browser access from the frontend.
- Used Pydantic models for request validation (`ToolRequest` and `ToolInfo`).
- Created `TOOL_REGISTRY` to map tool names to descriptions, inputs, outputs, and handler functions.
- Added health check, tool listing, and tool invocation endpoints.

## 3. Tool Logic and Placeholder Behavior

- Implemented placeholder tool functions in `mcp-server/tools.py`.
- Each tool returns structured JSON with `tool`, `summary`, and other output fields.
- Included a variety of assistant-style tools for code review, PPT generation, text summarization, AWS cost analysis, SQL generation, architecture guidance, and role-specific reviews.
- Added AWS Bedrock integration stub via `boto3` in `bedrock_text_generator`.
- Provided a fallback `assistant_agent` that uses Bedrock when enabled or a local echo response otherwise.

## 4. Frontend UI Development

- Built a static HTML/CSS/JavaScript frontend in `frontend/index.html`.
- Implemented two views: `Agent Chat` and `Tool Playground`.
- Added tool loading from the backend `/tools` endpoint.
- Added `/invoke` requests for tool execution and assistant chat.
- Designed the UI with responsive dark styling and interactive controls.

## 5. Containerization

- Added `mcp-server/Dockerfile` to package the backend into a container.
- Used `python:3.11-slim` as the base image.
- Installed dependencies, copied source code, exposed port `8000`, and set the `uvicorn` entrypoint.

## 6. Kubernetes Deployment

- Added `mcp-server/deployment.yaml` for the MCP server deployment.
- Added `mcp-server/service.yaml` for LoadBalancer service exposure.
- Defined one replica, container port mapping, and Kubernetes labels/selectors.

## 7. Deployment and Validation

- Built and pushed the Docker image to a registry.
- Applied Kubernetes manifests with `kubectl apply -f`.
- Verified deployment and service status using `kubectl get` commands.
- Confirmed the service endpoint by curling `/tools` and `/`.

## 8. GitHub and Version Control

- Used Git for source control.
- Committed changes locally and pushed to GitHub.
- Diagnosed authentication issues when HTTPS credentials failed and switched to SSH remote access successfully.

## 9. Documentation and Maintenance

- Maintained high-level documentation in `README.md` and `MCP_POC_DOCUMENTATION.md`.
- Added a dedicated codebase documentation file: `CODEBASE_DOCUMENTATION.md`.
- Added these two separate process and command files for clarity and future handoff.

## Summary

The current codebase follows a clear path from planning to implementation:
1. plan the MCP server proof-of-concept,
2. develop and register backend tools,
3. build a frontend for tool discovery and invocation,
4. package the backend in Docker,
5. deploy to Kubernetes, and
6. document the project and commands thoroughly.
