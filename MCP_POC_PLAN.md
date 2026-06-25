# MCP Server POC Plan

## Goal
Create a proof-of-concept MCP server project that demonstrates tool discovery and execution by an AI client.

## Objectives
- Learn and document the Model Context Protocol (MCP) architecture.
- Build a local MCP server with registered tools.
- Test tool discovery and invocation locally.
- Dockerize the server.
- Deploy to Amazon EKS.
- Connect an MCP-compatible AI client and verify end-to-end operation.

## Step 1: Understand MCP (1–2 hours)

### Key concepts
- MCP: protocol for AI clients to discover and invoke tools through a server.
- MCP Client: sends requests and discovers available tools.
- MCP Server: exposes tools and handles tool invocations.
- Tools: discrete capabilities registered by the MCP server.
- Resources/Prompts: metadata and guidance for tool usage.
- Tool discovery: client queries the server for available tools.
- Tool invocation: client calls a specific tool and receives a result.

### Data flow
1. AI Client
2. MCP Server
3. Available Tools
4. Execute Tool
5. Return Result

## Step 2: Development environment setup

### Required software
- Python 3.11+
- VS Code
- Git
- Docker Desktop
- Kubernetes CLI (`kubectl`)
- AWS CLI

### Create virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### Install MCP SDK
- Confirm SDK/version with the team.
- Install the package inside `.venv`.

## Step 3: Build the first MCP server

### Project structure
```
mcp-server/
├── server.py
├── tools.py
├── requirements.txt
└── README.md
```

### Server responsibilities
- Start an MCP server.
- Register tools.
- Wait for client requests.

## Step 4: Create tools

### Example tools
- `review_python_code` — review Python code for style, logic, best practices, and potential bugs.
- `create_ppt` — generate a PowerPoint outline or slide content from text input.
- `summarize_document` — summarize documents, reports, and long-form text with key points and action items.
- `aws_cost_analyzer` — analyze AWS cost data to identify spend patterns, savings opportunities, and optimization recommendations.
- `sql_generator` — generate SQL queries from natural language prompts or optimize existing SQL for performance.
- `architecture_diagram_generator` — create architecture diagram descriptions for cloud, application, or infrastructure designs.
- `frontend_developer` — review frontend code, UI/UX, accessibility, performance, and compatibility for client-side applications.
- `devops_engineer` — evaluate deployment, automation, CI/CD, infrastructure, and operational readiness for cloud-native systems.
- `quality_engineer` — assess test coverage, quality gates, validation, and reliability risks in software and development workflows.
- `backend_developer` — review backend architecture, API design, data models, security, and scalability for server-side systems.

### Tool behavior
- Accept input.
- Process the request.
- Return a structured output.

## Step 5: Register tools with the MCP server

### Server exposes
- Available tools list
- Tool metadata and descriptions
- Invocation endpoints

### Example tool registry
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

## Step 6: Test locally

### Run server
```bash
python server.py
```

### Verify
- Server starts successfully.
- AI client discovers tools.
- Each tool executes correctly.

## Step 7: Dockerize the server

### Create `Dockerfile`
- Base image with Python.
- Copy project files.
- Install requirements.
- Expose port.
- Run the server.

### Build and run
```bash
docker build -t mcp-server .
docker run -p 8000:8000 mcp-server
```

## Step 8: Deploy to Amazon EKS

### High-level flow
- Code → Docker Image → Amazon ECR → Amazon EKS → Pods → Service → Ingress

### Deployment steps
1. Build Docker image.
2. Push to Amazon ECR.
3. Create or use an existing EKS cluster.
4. Create Kubernetes manifest files: `deployment.yaml`, `service.yaml`.
5. Deploy using:
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```
6. Verify:
   ```bash
   kubectl get pods
   ```

## Step 9: Connect AI clients

- Connect an MCP-compatible client to the deployed server.
- Verify the client discovers available tools.
- Confirm tool invocation and response delivery.

## Step 10: Add more tools

### Suggested tools for POC
- Python code reviewer
- PowerPoint generator
- AWS cost analyzer
- CloudFormation/Terraform generator
- SQL optimizer
- Architecture diagram generator
- Documentation generator

## Suggested 2-day POC plan

### Day 1
- Learn MCP basics.
- Set up the project.
- Create an MCP server.
- Implement 2–3 simple tools.
- Test locally.

### Day 2
- Dockerize the application.
- Deploy to EKS.
- Verify tool discovery and execution.
- Document architecture and demo the POC.

## Notes
- A strong demo can use:
  - `review_python_code`
  - `create_ppt`
  - `aws_cost_analyzer`

- Keep the first version simple and testable.
- Iterate on tool coverage after the POC is working.
