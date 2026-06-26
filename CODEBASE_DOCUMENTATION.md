# MCP Setup Codebase Documentation

## Overview
This repository implements a minimal Model Context Protocol (MCP) proof-of-concept server with a browser-based frontend and Kubernetes deployment manifests for AWS EKS.

The project demonstrates:
- A FastAPI-based MCP tool server (`mcp-server/`)
- A lightweight JavaScript UI for tool discovery and invocation (`frontend/index.html`)
- Docker packaging and Kubernetes deployment on AWS EKS
- Placeholder AI and automation tools for code review, documentation, DevOps, and AWS cost analysis

## Repository Layout

- `README.md` - high-level project summary and quick start guidance
- `MCP_POC_DOCUMENTATION.md` - existing POC documentation and deployment notes
- `MCP_POC_PLAN.md` - planning notes for the POC
- `frontend/` - static browser UI for interacting with the MCP server
- `mcp-server/` - FastAPI server, tooling logic, Dockerfile, and Kubernetes manifests

## Backend: `mcp-server/`

### `server.py`
The server exposes three HTTP endpoints:

- `GET /` - health check
- `GET /tools` - returns a discovery list of all registered tools
- `POST /invoke` - invokes a named tool with the provided input

Key behaviors:
- Registers tools in `TOOL_REGISTRY`
- Uses Pydantic models for request validation
- Adds CORS middleware to allow browser-based clients to access the API
- Returns structured JSON results for each tool

### Tool registry
`TOOL_REGISTRY` maps tool names to:
- `description`
- `inputs`
- `outputs`
- `function`

Registered tools include:
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

### `tools.py`
This module implements the tool logic. Most tools are placeholders that demonstrate response structure and basic behavior.

Important details:
- `review_python_code` checks for wildcard imports, `print()` usage, and TODO/FIXME comments
- `create_ppt` returns a sample slide outline
- `summarize_document` extracts text summary and key points
- `aws_cost_analyzer` inspects AWS-related text and suggests cost optimizations
- `sql_generator` returns a sample SQL query template
- `architecture_diagram_generator` returns architecture guidance steps
- `frontend_developer`, `devops_engineer`, `quality_engineer`, `backend_developer` return simple review recommendations based on string content
- `bedrock_text_generator` calls AWS Bedrock via `boto3` using `BEDROCK_MODEL_ID` and `AWS_REGION`
- `assistant_agent` either forwards user input to Bedrock or uses a local fallback echo response depending on `BEDROCK_ENABLED`

### `requirements.txt`
Lists the Python runtime dependencies:
- `fastapi`
- `uvicorn`
- `pydantic`
- `boto3`

### `Dockerfile`
Builds the MCP server container:
- Base image: `python:3.11-slim`
- Copies requirements and installs dependencies
- Copies the application code into `/app`
- Exposes port `8000`
- Runs `uvicorn server:app --host 0.0.0.0 --port 8000`

## Frontend: `frontend/index.html`

The frontend is a single-page static UI with two main views:

1. **Agent Chat**
   - Allows the user to send a message to the `assistant_agent` tool
   - Displays a chat-style conversation
   - Uses the same backend `/invoke` endpoint for the assistant tool

2. **Tool Playground**
   - Loads available tools from `GET /tools`
   - Lets the user choose a tool and submit input text
   - Sends `POST /invoke` requests and displays the JSON response

Frontend implementation details:
- Uses vanilla JavaScript and DOM manipulation
- Has a custom dark UI with CSS variables
- Defines `apiBase` as a hard-coded backend URL
- Handles tool loading, invocation, and chat interaction
- Includes basic error handling for API failures

> Note: The current `apiBase` value in `frontend/index.html` points to a specific ELB address. Update this if your deployment endpoint changes.

## Kubernetes Deployment

### `mcp-server/deployment.yaml`
Defines a Kubernetes Deployment for the MCP server:
- `replicas: 1`
- `selector.matchLabels: app: mcp-server`
- Single container named `mcp-server`
- Uses image `709097783069.dkr.ecr.us-east-1.amazonaws.com/mcp-server:latest`
- Exposes container port `8000`

### `mcp-server/service.yaml`
Defines a Service to expose the deployment:
- `type: LoadBalancer`
- Selects pods with `app: mcp-server`
- Exposes port `8000` and forwards to container port `8000`

## Running Locally

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install backend dependencies:
   ```bash
   pip install -r mcp-server/requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   cd mcp-server
   uvicorn server:app --reload --host 0.0.0.0 --port 8000
   ```

4. Serve the frontend locally (for example):
   ```bash
   cd frontend
   python -m http.server 8000
   ```

5. Open the frontend in a browser and ensure `apiBase` points to the running backend.

## Deployment Flow

1. Build the Docker image from `mcp-server/`:
   ```bash
   docker build -t mcp-server .
   ```

2. Tag and push the image to your container registry:
   ```bash
   docker tag mcp-server:latest <your-registry>/mcp-server:latest
   docker push <your-registry>/mcp-server:latest
   ```

3. Update `mcp-server/deployment.yaml` if the image reference changes.

4. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f mcp-server/deployment.yaml
   kubectl apply -f mcp-server/service.yaml
   ```

5. Verify the deployment:
   ```bash
   kubectl get deployments
   kubectl get pods
   kubectl get svc
   kubectl rollout status deployment/mcp-server
   ```

## What Has Been Implemented

- A working MCP server with tool discovery and invocation endpoints
- A tool registry architecture for adding new AI tools
- Placeholder implementations for multiple AI-style tools
- A static frontend with both chat and tool playground experiences
- Docker packaging for containerized deployment
- Kubernetes manifests for EKS deployment behind a LoadBalancer
- AWS Bedrock integration scaffolding via `boto3`
- CORS-enabled API to support browser clients

## Next Improvements

Potential next steps include:
- Replace placeholder tool implementations with real AI model calls
- Add authentication and authorization for tool invocation
- Externalize the frontend backend URL configuration
- Add unit tests for backend tools and API behavior
- Add CI/CD automation for Docker build and Kubernetes deployment
- Improve frontend UX, validation, and tool-specific input forms
