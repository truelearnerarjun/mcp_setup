# MCP Server POC Documentation

## Overview
This POC demonstrates a simple Model Context Protocol (MCP) server running on AWS EKS, with tools registered for AI client discovery and invocation.

The architecture includes:
- `mcp-server/` — FastAPI-based MCP tool server
- `frontend/` — browser UI for tool selection and invocation
- AWS ECR — container registry for the Docker image
- AWS EKS — Kubernetes cluster hosting the MCP server

## Project structure

```
/mcp_setup
├── MCP_POC_PLAN.md
├── MCP_POC_DOCUMENTATION.md
├── README.md
├── frontend/
│   └── index.html
└── mcp-server/
    ├── Dockerfile
    ├── README.md
    ├── deployment.yaml
    ├── requirements.txt
    ├── server.py
    ├── service.yaml
    └── tools.py
```

## Components

### MCP Server
- `mcp-server/server.py` exposes:
  - `GET /` health check
  - `GET /tools` tool discovery
  - `POST /invoke` tool invocation
- `mcp-server/tools.py` defines tool handlers such as:
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

### Frontend
- `frontend/index.html` provides a minimal browser UI
- It loads available tools from `/tools`
- It sends `POST /invoke` requests with tool and input
- It displays tool output in the browser

## Deployment flow

1. Build the Docker image:
   ```bash
   docker build -t mcp-server .
   ```
2. Push the image to ECR:
   ```bash
   docker tag mcp-server:latest 709097783069.dkr.ecr.us-east-1.amazonaws.com/mcp-server:latest
   docker push 709097783069.dkr.ecr.us-east-1.amazonaws.com/mcp-server:latest
   ```
3. Update the Kubernetes deployment image:
   - `mcp-server/deployment.yaml` contains the ECR image reference
4. Deploy to EKS:
   ```bash
   kubectl apply -f /workspaces/mcp_setup/mcp-server/deployment.yaml
   kubectl apply -f /workspaces/mcp_setup/mcp-server/service.yaml
   ```

## Verification

### Confirm deployment
```bash
kubectl get deployments
kubectl get pods
kubectl get svc
```

### Verify service endpoint
Use the `LoadBalancer` hostname from `kubectl get svc`:
```bash
curl http://<external-dns>:8000/tools
curl http://<external-dns>:8000/
```

### Invoke a tool manually
```bash
curl -X POST "http://<external-dns>:8000/invoke" \
  -H "Content-Type: application/json" \
  -d '{"tool":"review_python_code","input":"import os\nprint(\"hello\")"}'
```

## Browser frontend usage

1. Open `frontend/index.html` in a browser
2. Select a tool from the dropdown
3. Enter input text
4. Click `Run Tool`
5. View the returned result in the output pane

> Note: The frontend currently points to the deployed EKS LoadBalancer URL. Update `apiBase` in `frontend/index.html` if the endpoint changes.

## Notes

- CORS support was enabled in `mcp-server/server.py` to allow browser access.
- This POC is intentionally minimal so you can iterate on tools and UI quickly.
- The server can be extended with richer tool behaviors and better input validation.
