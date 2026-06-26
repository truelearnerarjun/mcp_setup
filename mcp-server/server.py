from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List

from tools import (
    architecture_diagram_generator,
    assistant_agent,
    aws_cost_analyzer,
    backend_developer,
    bedrock_text_generator,
    create_ppt,
    devops_engineer,
    frontend_developer,
    quality_engineer,
    review_python_code,
    sql_generator,
    summarize_document,
)

app = FastAPI(title="MCP Server POC")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ToolRequest(BaseModel):
    tool: str
    input: str


class ToolInfo(BaseModel):
    name: str
    description: str
    inputs: List[str]
    outputs: List[str]


TOOL_REGISTRY = {
    "review_python_code": {
        "description": "Review Python code for style, logic, best practices, and potential bugs.",
        "inputs": ["code"],
        "outputs": ["summary", "issues"],
        "function": review_python_code,
    },
    "create_ppt": {
        "description": "Generate a PowerPoint slide outline from text input.",
        "inputs": ["text"],
        "outputs": ["summary", "slides"],
        "function": create_ppt,
    },
    "summarize_document": {
        "description": "Summarize documents and long-form text with key points and action items.",
        "inputs": ["text"],
        "outputs": ["summary", "key_points", "recommendation"],
        "function": summarize_document,
    },
    "aws_cost_analyzer": {
        "description": "Analyze AWS cost data and provide optimization insights.",
        "inputs": ["data"],
        "outputs": ["summary", "insights"],
        "function": aws_cost_analyzer,
    },
    "sql_generator": {
        "description": "Generate or optimize SQL queries based on natural language prompts.",
        "inputs": ["prompt"],
        "outputs": ["summary", "query", "notes"],
        "function": sql_generator,
    },
    "architecture_diagram_generator": {
        "description": "Create architecture diagram descriptions for cloud and application designs.",
        "inputs": ["description"],
        "outputs": ["summary", "diagram_steps", "recommendation"],
        "function": architecture_diagram_generator,
    },
    "frontend_developer": {
        "description": "Review frontend code, UI/UX, accessibility, performance, and compatibility.",
        "inputs": ["input_text"],
        "outputs": ["summary", "recommendations"],
        "function": frontend_developer,
    },
    "devops_engineer": {
        "description": "Evaluate deployment, automation, CI/CD, infrastructure, and operational readiness.",
        "inputs": ["input_text"],
        "outputs": ["summary", "recommendations"],
        "function": devops_engineer,
    },
    "quality_engineer": {
        "description": "Assess test coverage, quality gates, validation, and reliability risks.",
        "inputs": ["input_text"],
        "outputs": ["summary", "observations"],
        "function": quality_engineer,
    },
    "backend_developer": {
        "description": "Review backend architecture, API design, data models, security, and scalability.",
        "inputs": ["input_text"],
        "outputs": ["summary", "suggestions"],
        "function": backend_developer,
    },
    "bedrock_text_generator": {
        "description": "Generate text using AWS Bedrock models for flexible assistant responses.",
        "inputs": ["prompt"],
        "outputs": ["tool", "model_id", "response"],
        "function": bedrock_text_generator,
    },
    "assistant_agent": {
        "description": "Run an assistant-style agent backed by Bedrock or a local fallback.",
        "inputs": ["input_text"],
        "outputs": ["summary", "assistant_response"],
        "function": assistant_agent,
    },
}


@app.get("/tools", response_model=List[ToolInfo])
def list_tools() -> List[ToolInfo]:
    return [
        ToolInfo(
            name=name,
            description=info["description"],
            inputs=info["inputs"],
            outputs=info["outputs"],
        )
        for name, info in TOOL_REGISTRY.items()
    ]


@app.post("/invoke")
def invoke_tool(request: ToolRequest) -> Dict[str, Any]:
    tool_info = TOOL_REGISTRY.get(request.tool)
    if not tool_info:
        raise HTTPException(status_code=404, detail="Tool not found")

    result = tool_info["function"](request.input)
    return {
        "tool": request.tool,
        "input": request.input,
        "result": result,
    }


@app.get("/")
def health_check() -> Dict[str, str]:
    return {"status": "ok", "message": "MCP Server is running."}
