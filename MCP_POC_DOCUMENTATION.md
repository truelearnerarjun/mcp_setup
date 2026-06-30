# MCP Server POC Documentation

## Overview
This repository contains a FastAPI-based MCP server, a browser frontend, and Kubernetes manifests for deploying the backend on EKS.

The current implementation supports:
- Tool discovery through `GET /tools`
- Tool invocation through `POST /invoke`
- Document upload and summarization through `POST /summarize-file`
- Browser chat for skills-related prompts only
- Local fallback behavior when Bedrock is disabled

## What The App Actually Does

### Agent chat
- Accepts only skills-related prompts
- Allows code review, PPT generation, summarization, SQL help, architecture diagrams, frontend/backend review, DevOps review, quality review, and Bedrock text generation
- Rejects unrelated prompts outside the registered MCP skill scope

### File summarization
- Accepts `.txt`, `.pdf`, and `.docx` uploads
- Extracts text from the uploaded file
- Filters obvious contact and metadata noise from summaries
- Produces a short summary plus key points

### Backend behavior
- Reads full document content with a configurable extraction cap
- Uses threadpool execution for upload extraction and summarization
- Supports Bedrock-backed responses when `BEDROCK_ENABLED=true`
- Falls back to local summaries and reviews when Bedrock is disabled or unavailable

## Deployment Model

The backend is meant to run in Kubernetes on EKS:
- `mcp-server/deployment.yaml` runs the container
- `mcp-server/service.yaml` exposes the service internally
- `mcp-server/ingress.yaml` routes traffic through an AWS ALB
- `mcp-server/rbac.yaml` provides the service account and Bedrock role annotation

## Local Development

For local testing:
- Run the backend on `http://localhost:8000`
- Serve the frontend separately on `http://localhost:3000`
- Switch `frontend/index.html` to the local backend URL only when developing locally

## API Endpoints

- `GET /` - health check
- `GET /tools` - list registered MCP tools
- `POST /invoke` - invoke a tool by name
- `POST /summarize-file` - upload and summarize a `.txt`, `.pdf`, or `.docx` file

## Notes

- The frontend has a commented local backend URL and an ALB URL placeholder for deployment.
- The summary endpoint is optimized for readable text extraction, but scanned PDFs may still require OCR outside this repo.
