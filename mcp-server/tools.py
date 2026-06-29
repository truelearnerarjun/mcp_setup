import os
import re

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from typing import Any, Dict, List


SKILL_KEYWORDS = [
    "review", "code", "python", "bug", "debug", "tool", "prompt", "summarize",
    "document", "architecture", "diagram", "aws", "cost", "sql", "query",
    "frontend", "backend", "devops", "deploy", "deployment", "test", "quality",
    "agent", "assistant", "mcp", "skill", "design", "api", "database"
]


def is_skill_related(text: str) -> bool:
    """Return True only when the prompt appears to request a software engineering or tool-related task."""
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    if not normalized:
        return False
    tokens = set(normalized.split())
    return bool(tokens & set(SKILL_KEYWORDS)) or any(keyword in normalized for keyword in ["review", "summarize", "design", "deploy", "backend", "frontend", "sql", "python", "aws"])


def review_python_code(code: str) -> Dict[str, Any]:
    """Simple placeholder for a Python review tool."""
    issues: List[str] = []
    if "import *" in code:
        issues.append("Avoid using wildcard imports.")
    if "print(" in code and "#" not in code:
        issues.append("Consider using logging instead of print for production code.")
    if "TODO" in code or "FIXME" in code:
        issues.append("Remove or resolve TODO/FIXME comments before production.")

    return {
        "tool": "review_python_code",
        "summary": "Python code review completed.",
        "issues": issues or ["No obvious issues found."],
    }


def create_ppt(text: str) -> Dict[str, Any]:
    """Simple placeholder for a PowerPoint generation tool."""
    return {
        "tool": "create_ppt",
        "summary": "Generated a slide outline from the input text.",
        "slides": [
            {"title": "Overview", "content": text[:150]},
            {"title": "Key Points", "content": "Summarize the main ideas and next steps."},
        ],
    }


def summarize_document(text: str) -> Dict[str, Any]:
    """Summarize a document or long-form text."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    key_points = [paragraphs[0][:120]] if paragraphs else [text[:120]]
    return {
        "tool": "summarize_document",
        "summary": "Document summary created.",
        "key_points": key_points,
        "recommendation": "Review the full text for details beyond the summary.",
    }


def aws_cost_analyzer(data: str) -> Dict[str, Any]:
    """Simple placeholder for an AWS cost analysis tool."""
    insights = [
        "Review high-cost services such as EC2 and RDS.",
        "Check for idle or underutilized resources.",
    ]
    if "S3" in data:
        insights.append("Investigate S3 storage class usage and lifecycle policies.")
    return {
        "tool": "aws_cost_analyzer",
        "summary": "Analyzed cost data and returned a high-level summary.",
        "insights": insights,
    }


def sql_generator(prompt: str) -> Dict[str, Any]:
    """Generate or improve SQL queries based on the prompt."""
    sample_query = "SELECT * FROM table_name WHERE condition;"
    return {
        "tool": "sql_generator",
        "summary": "Generated SQL query guidance.",
        "query": sample_query,
        "notes": [
            "Replace `table_name` with the target table.",
            "Adjust `condition` to match the filtering criteria.",
        ],
    }


def architecture_diagram_generator(description: str) -> Dict[str, Any]:
    """Create a high-level architecture diagram description."""
    return {
        "tool": "architecture_diagram_generator",
        "summary": "Created architecture diagram steps.",
        "diagram_steps": [
            "Identify major components.",
            "Define data flow between components.",
            "Specify cloud services and interfaces.",
        ],
        "recommendation": "Use a diagramming tool to visualize this architecture.",
    }


def frontend_developer(input_text: str) -> Dict[str, Any]:
    """Review frontend development concerns."""
    issues: List[str] = []
    if "accessibility" not in input_text.lower():
        issues.append("Check accessibility for keyboard navigation and screen readers.")
    if "performance" not in input_text.lower():
        issues.append("Evaluate frontend performance, bundle size, and rendering speed.")
    return {
        "tool": "frontend_developer",
        "summary": "Reviewed frontend considerations.",
        "recommendations": issues or ["Frontend review completed with no major concerns detected."],
    }


def devops_engineer(input_text: str) -> Dict[str, Any]:
    """Review DevOps and deployment practices."""
    recommendations: List[str] = []
    if "CI" not in input_text and "ci" not in input_text:
        recommendations.append("Add CI/CD validation for automated testing and deployment.")
    if "infrastructure" not in input_text.lower():
        recommendations.append("Define infrastructure-as-code and environment configuration.")
    return {
        "tool": "devops_engineer",
        "summary": "Reviewed DevOps readiness.",
        "recommendations": recommendations or ["DevOps review completed with no major concerns detected."],
    }


def quality_engineer(input_text: str) -> Dict[str, Any]:
    """Review quality engineering practices."""
    observations: List[str] = []
    if "test" not in input_text.lower():
        observations.append("Recommend adding unit and integration tests for key logic.")
    if "monitor" not in input_text.lower() and "monitoring" not in input_text.lower():
        observations.append("Include monitoring and validation checks in the workflow.")
    return {
        "tool": "quality_engineer",
        "summary": "Reviewed quality engineering practices.",
        "observations": observations or ["Quality review completed with no major concerns detected."],
    }


def backend_developer(input_text: str) -> Dict[str, Any]:
    """Review backend architecture and API design."""
    suggestions: List[str] = []
    if "database" not in input_text.lower():
        suggestions.append("Clarify data storage design and database choice.")
    if "api" not in input_text.lower():
        suggestions.append("Document API contracts and error handling behavior.")
    return {
        "tool": "backend_developer",
        "summary": "Reviewed backend system design.",
        "suggestions": suggestions or ["Backend review completed with no major concerns detected."],
    }


def bedrock_text_generator(prompt: str) -> Dict[str, Any]:
    """Call AWS Bedrock text generation to respond to the prompt."""
    model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-text-2")
    region = os.getenv("AWS_REGION", "us-east-1")
    try:
        client = boto3.client("bedrock", region_name=region)
        response = client.invoke_model(
            modelId=model_id,
            contentType="text/plain",
            accept="application/json",
            body=prompt.encode("utf-8"),
        )
        body = response["body"].read().decode("utf-8")
        return {
            "tool": "bedrock_text_generator",
            "model_id": model_id,
            "response": body,
        }
    except (BotoCoreError, ClientError) as exc:
        return {
            "tool": "bedrock_text_generator",
            "error": "Bedrock call failed.",
            "details": str(exc),
        }


def assistant_agent(input_text: str) -> Dict[str, Any]:
    """A guardrailed assistant tool that only answers skill-related prompts."""
    if not is_skill_related(input_text):
        return {
            "tool": "assistant_agent",
            "summary": "Guardrail triggered: off-scope prompt.",
            "assistant_response": "I can only help with skill-related or MCP-tool requests such as code review, architecture, deployment, testing, or documentation tasks.",
        }

    if os.getenv("BEDROCK_ENABLED", "true").lower() in ("true", "1", "yes"):
        prompt = "You are a helpful assistant restricted to skill-related software engineering tasks. Answer only if the user asks about code review, architecture, deployment, testing, documentation, or similar engineering topics. Otherwise refuse politely. User input:\n\n" + input_text
        bedrock_result = bedrock_text_generator(prompt)
        if bedrock_result.get("response"):
            return {
                "tool": "assistant_agent",
                "summary": "Bedrock-powered assistant response.",
                "assistant_response": bedrock_result["response"],
            }
        return {
            "tool": "assistant_agent",
            "error": "Assistant agent Bedrock call failed.",
            "details": bedrock_result.get("details"),
        }
    return {
        "tool": "assistant_agent",
        "summary": "Local fallback assistant response.",
        "assistant_response": f"Skill-related assistance: {input_text}",
    }
