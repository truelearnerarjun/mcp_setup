# Run Project

Use these steps to run the frontend locally with the backend running on EKS through the AWS ALB.

## 1. Start The Frontend

Open PowerShell and run:

```powershell
cd F:\mcp_setup\mcp_setup
python -m http.server 3000
```

Open this URL in the browser:

```text
http://localhost:3000/frontend/
```

The frontend is configured in `frontend/index.html` to call the deployed ALB backend:

```text
http://k8s-default-mcpserve-9572bfb994-1376550949.us-east-1.elb.amazonaws.com
```

## 2. Check The Live Backend

Run these commands from the project root:

```powershell
cd F:\mcp_setup\mcp_setup
kubectl get pods
kubectl get ingress
curl http://k8s-default-mcpserve-9572bfb994-1376550949.us-east-1.elb.amazonaws.com/
```

Expected health response:

```json
{"status":"ok","message":"MCP Server is running."}
```

## 3. Test Agent Chat API

```powershell
$body = @{
  tool = "assistant_agent"
  input = "print('arjun') review this code"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://k8s-default-mcpserve-9572bfb994-1376550949.us-east-1.elb.amazonaws.com/invoke" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## 4. Redeploy Backend After Code Changes

Make sure Docker Desktop is running, then run:

```powershell
cd F:\mcp_setup\mcp_setup

aws eks update-kubeconfig --region us-east-1 --name mcp-server

aws ecr get-login-password --region us-east-1 |
  docker login --username AWS --password-stdin 709097783069.dkr.ecr.us-east-1.amazonaws.com

docker build -t 709097783069.dkr.ecr.us-east-1.amazonaws.com/mcp-server:latest .\mcp-server

docker push 709097783069.dkr.ecr.us-east-1.amazonaws.com/mcp-server:latest

kubectl rollout restart deployment/mcp-server
kubectl rollout status deployment/mcp-server
```

## 5. Useful Kubernetes Commands

```powershell
kubectl get pods -l app=mcp-server
kubectl logs deployment/mcp-server --tail=100
kubectl describe ingress mcp-server
kubectl get svc
```

## 6. Run Backend Locally Instead

Only use this if you want to test without EKS.

```powershell
cd F:\mcp_setup\mcp_setup\mcp-server
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Then change `frontend/index.html` temporarily:

```js
const apiBase = 'http://localhost:8000';
```

Change it back to the ALB URL before using the EKS backend again.

## Notes

- Use `http://localhost:3000/frontend/`, not only `http://localhost:3000/`.
- The Chrome DevTools request to `/.well-known/appspecific/com.chrome.devtools.json` can be ignored.
- If the browser shows an old error after deployment, hard refresh with `Ctrl + Shift + R`.
- The current ALB listens on port `80`, so do not add `:8000` to the ALB URL.
