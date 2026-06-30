# Project Process

## Overview
This document describes the process followed while building the MCP setup codebase. The project implemented a minimal MCP server, a static frontend, Docker packaging, and Kubernetes deployment support.

## Step 1: Define the architecture
- Identify the two main components:
  - `mcp-server/` for backend tool serving
  - `frontend/` for browser-based interaction
- Plan the server API surface:
  - `GET /` health check
  - `GET /tools` tool discovery
  - `POST /invoke` tool invocation

## Step 2: Build the backend service
- Create `server.py` using FastAPI
- Add CORS middleware for browser connectivity
- Define `ToolRequest` and `ToolInfo` models with Pydantic
- Build a `TOOL_REGISTRY` mapping tool names to implementations
- Implement placeholder tools in `tools.py` to verify behavior
- Add AWS Bedrock integration scaffolding using `boto3`

## Step 3: Create the frontend UI
- Build `frontend/index.html` as a single-page application
- Add a sidebar with two views:
  - Agent Chat
  - Tool Playground
- Implement tool discovery via `/tools`
- Implement tool invocation via `/invoke`
- Add a chat interface that uses the `assistant_agent` tool
- Hard-code `apiBase` to the deployed backend endpoint for ease of testing

## Step 4: Containerize the application
- Add `mcp-server/Dockerfile`
- Use `python:3.11-slim` as the base image
- Install Python dependencies from `requirements.txt`
- Copy application files into the container
- Expose port `8000`
- Configure `uvicorn` as the container entrypoint

## Step 5: Prepare Kubernetes deployment
- Create `mcp-server/deployment.yaml` for the MCP server deployment
- Create `mcp-server/service.yaml` to expose the service via LoadBalancer
- Reference the ECR image in the deployment manifest
- Use `app: mcp-server` labels for selector consistency

## Step 6: Test locally and deploy
- Run the backend with `uvicorn` locally
- Serve the frontend using a local HTTP server
- Verify the frontend can reach the backend and show tools
- Build and push the Docker image
- Apply Kubernetes manifests to deploy to EKS
- Validate the deployment with `kubectl get pods`, `kubectl get svc`, and `kubectl rollout status`

## Step 7: Document the project
- Add high-level documentation in `README.md`
- Maintain detailed POC notes in `MCP_POC_DOCUMENTATION.md`
- Add complete codebase documentation in `CODEBASE_DOCUMENTATION.md`
- Add these new files for commands and process documentation

## Summary of the process followed
1. Architect the MCP server and frontend split.
2. Implement backend API and tool registry.
3. Implement frontend UX and backend integration.
4. Containerize the application with Docker.
5. Add Kubernetes manifests for deployment.
6. Test locally, build the image, push it, and deploy on EKS.
7. Document the codebase and workflow for future updates.
