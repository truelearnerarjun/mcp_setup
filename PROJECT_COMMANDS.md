# Project Commands

Common commands for running, testing, building, and deploying this MCP project.

## Project Paths

```powershell
cd F:\mcp_setup\mcp_setup
```

Backend:

```powershell
cd F:\mcp_setup\mcp_setup\mcp-server
```

Frontend:

```powershell
cd F:\mcp_setup\mcp_setup\frontend
```

## Run Locally

### Backend

Create and activate the virtual environment:

```powershell
cd F:\mcp_setup\mcp_setup\mcp-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the FastAPI backend:

```powershell
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Backend URLs:

```text
http://localhost:8000
http://localhost:8000/tools
```

### Frontend

Run the static frontend on a different port:

```powershell
cd F:\mcp_setup\mcp_setup\frontend
python -m http.server 3000
```

Open:

```text
http://localhost:3000
```

Make sure `frontend/index.html` points to the local backend only for local development:

```js
// const apiBase = 'http://localhost:8000';
const apiBase = 'http://k8s-default-mcpserve-9572bfb994-1376550949.us-east-1.elb.amazonaws.com';
```

## Environment Variables

Run with Bedrock enabled:

```powershell
$env:BEDROCK_ENABLED="true"
$env:BEDROCK_MODEL_ID="amazon.nova-pro-v1:0"
$env:AWS_REGION="us-east-1"
```

Run without Bedrock, using local fallback responses:

```powershell
$env:BEDROCK_ENABLED="false"
```

## API Checks

Health check:

```powershell
curl http://localhost:8000/
```

List tools:

```powershell
curl http://localhost:8000/tools
```

Invoke agent chat:

```powershell
curl -X POST http://localhost:8000/invoke `
  -H "Content-Type: application/json" `
  -d "{\"tool\":\"assistant_agent\",\"input\":\"create a ppt on animals\"}"
```

Invoke Python code review:

```powershell
curl -X POST http://localhost:8000/invoke `
  -H "Content-Type: application/json" `
  -d "{\"tool\":\"review_python_code\",\"input\":\"import os\nprint('hello')\"}"
```

Upload and summarize a text file:

```powershell
curl -X POST http://localhost:8000/summarize-file `
  -F "file=@sample.txt" `
  -F "instruction=summarize this document"
```

Supported summary uploads:

```text
.txt
.pdf
.docx
```

## Validate Code

Compile-check backend files:

```powershell
cd F:\mcp_setup\mcp_setup\mcp-server
python -m py_compile server.py tools.py
```

Check required Python packages:

```powershell
python -c "import fastapi, boto3, pypdf, docx; print('imports ok')"
```

## Docker

Build the backend image:

```powershell
cd F:\mcp_setup\mcp_setup\mcp-server
docker build -t mcp-server .
```

Run the image locally:

```powershell
docker run --rm -p 8000:8000 `
  -e BEDROCK_ENABLED=false `
  mcp-server
```

Tag for Amazon ECR:

```powershell
docker tag mcp-server:latest 709097783069.dkr.ecr.us-east-1.amazonaws.com/mcp-server:latest
```

Login to ECR:

```powershell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 709097783069.dkr.ecr.us-east-1.amazonaws.com
```

Push to ECR:

```powershell
docker push 709097783069.dkr.ecr.us-east-1.amazonaws.com/mcp-server:latest
```

## Kubernetes

Apply RBAC, deployment, service, and ALB ingress:

```powershell
cd F:\mcp_setup\mcp_setup
kubectl apply -f mcp-server/rbac.yaml
kubectl apply -f mcp-server/deployment.yaml
kubectl apply -f mcp-server/service.yaml
kubectl apply -f mcp-server/ingress.yaml
```

Check rollout:

```powershell
kubectl rollout status deployment/mcp-server
```

Check resources:

```powershell
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl get ingress
```

View backend logs:

```powershell
kubectl logs deployment/mcp-server
```

Restart deployment after pushing a new `latest` image:

```powershell
kubectl rollout restart deployment/mcp-server
kubectl rollout status deployment/mcp-server
```

Get the ALB hostname or URL:

```powershell
kubectl get ingress mcp-server
```

Test deployed backend:

```powershell
curl http://<alb-host>/tools
```

## Git

Check status:

```powershell
git status --short
```

Stage files:

```powershell
git add PROJECT_COMMANDS.md mcp-server/server.py mcp-server/tools.py mcp-server/requirements.txt frontend/index.html
```

Commit:

```powershell
git commit -m "Update MCP app commands and document upload support"
```

Push:

```powershell
git push origin main
```
