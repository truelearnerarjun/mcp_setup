# Important Commands

## Local development

### Create and activate Python virtual environment
```powershell
cd f:\mcp_setup\mcp_setup\mcp-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install Python dependencies
```powershell
pip install -r requirements.txt
```

### Run the FastAPI server locally
```powershell
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Serve the frontend locally
```powershell
cd f:\mcp_setup\mcp_setup\frontend
python -m http.server 8000
```

## Docker and container image

### Build the Docker image
```powershell
cd f:\mcp_setup\mcp_setup\mcp-server
docker build -t mcp-server .
```

### Tag the Docker image for registry push
```powershell
docker tag mcp-server:latest <your-registry>/mcp-server:latest
```

### Push the Docker image to registry
```powershell
docker push <your-registry>/mcp-server:latest
```

## Kubernetes deployment

### Deploy the Kubernetes resources
```powershell
kubectl apply -f f:\mcp_setup\mcp_setup\mcp-server\deployment.yaml
kubectl apply -f f:\mcp_setup\mcp_setup\mcp-server\service.yaml
```

### Check deployment status
```powershell
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl rollout status deployment/mcp-server
```

## Git commands

### Check current repository state
```powershell
git status --short
```

### Add modified files
```powershell
git add <file-path>
```

### Commit changes
```powershell
git commit -m "Your commit message"
```

### Push to GitHub via SSH
```powershell
git push origin main
```

### Switch Git remote to SSH
```powershell
git remote set-url origin git@github.com:truelearnerarjun/mcp_setup.git
```

## AWS Bedrock / environment variables

### Example environment variables for Bedrock tools
```powershell
$env:BEDROCK_ENABLED="true"
$env:BEDROCK_MODEL_ID="amazon.titan-text-2"
$env:AWS_REGION="us-east-1"
```
# Important Commands

This file lists the key commands used for running, building, deploying, and managing the MCP codebase.

## Local Python Backend

Set up a Python virtual environment:
```bash
python -m venv .venv
```
Activate the virtual environment:
- Windows PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

Install backend dependencies:
```bash
pip install -r mcp-server/requirements.txt
```

Run the FastAPI server locally:
```bash
cd mcp-server
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## Local Frontend

Serve the frontend files locally:
```bash
cd frontend
python -m http.server 8000
```

Open the browser at:
```text
http://localhost:8000
```

## Docker

Build the Docker image:
```bash
cd mcp-server
docker build -t mcp-server .
```

Tag the image for your registry:
```bash
docker tag mcp-server:latest <your-registry>/mcp-server:latest
```

Push the image to the registry:
```bash
docker push <your-registry>/mcp-server:latest
```

## Kubernetes

Apply the deployment manifest:
```bash
kubectl apply -f mcp-server/deployment.yaml
```

Apply the service manifest:
```bash
kubectl apply -f mcp-server/service.yaml
```

Check deployment status:
```bash
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl rollout status deployment/mcp-server
```

## Git / GitHub

Check repository status:
```bash
git status
```

Stage changes:
```bash
git add <files>
```

Commit changes:
```bash
git commit -m "Your message"
```

Push changes to GitHub (SSH remote recommended):
```bash
git push origin main
```

If remote is HTTPS and credentials fail, switch to SSH:
```bash
git remote set-url origin git@github.com:truelearnerarjun/mcp_setup.git
```

## API Validation

List available tools:
```bash
curl http://<backend-host>:8000/tools
```

Invoke a tool:
```bash
curl -X POST http://<backend-host>:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"tool": "review_python_code", "input": "import os\nprint(\"hello\")"}'
```
