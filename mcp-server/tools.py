import json
import os
import re

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from typing import Any, Dict, List


SKILL_GUARDRAIL_MESSAGE = (
    "I can only help with questions about the registered MCP skills: "
    "Python code review, PowerPoint outline creation, document summarization, "
    "AWS cost analysis, SQL generation, architecture diagrams, frontend development, "
    "DevOps, quality engineering, backend development, and Bedrock text generation."
)

REGISTERED_MCP_SKILLS = {
    "review_python_code": [
        "review python code",
        "python code review",
        "review this code",
        "check this code",
        "analyze this code",
        "fix this code",
        "improve this code",
        "python",
        "code review",
    ],
    "create_ppt": [
        "create ppt",
        "ppt",
        "make ppt",
        "need ppt",
        "need a ppt",
        "powerpoint",
        "presentation",
        "slide",
        "slides",
    ],
    "summarize_document": [
        "summarize document",
        "document summary",
        "summarization",
        "summarize",
    ],
    "aws_cost_analyzer": [
        "aws cost",
        "cost analyzer",
        "cost analysis",
        "aws billing",
    ],
    "sql_generator": [
        "sql",
        "sql generator",
        "query",
        "database query",
    ],
    "architecture_diagram_generator": [
        "architecture diagram",
        "architecture",
        "diagram",
        "cloud design",
    ],
    "frontend_developer": [
        "frontend",
        "front end",
        "ui",
        "ux",
        "accessibility",
    ],
    "devops_engineer": [
        "devops",
        "ci/cd",
        "deployment",
        "infrastructure",
        "kubernetes",
        "docker",
    ],
    "quality_engineer": [
        "quality",
        "qa",
        "testing",
        "test coverage",
        "validation",
    ],
    "backend_developer": [
        "backend",
        "back end",
        "api",
        "server",
        "scalability",
    ],
    "bedrock_text_generator": [
        "bedrock",
        "aws bedrock",
        "text generation",
        "llm",
    ],
}

REGISTERED_SKILL_LIST_REQUESTS = {
    "what skills",
    "which skills",
    "available skills",
    "registered skills",
    "supported skills",
    "what can you help",
}


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9+#.]+", " ", text.lower()).strip()


def contains_any(normalized_text: str, phrases: List[str]) -> bool:
    return any(normalize_text(phrase) in normalized_text for phrase in phrases)


GENERAL_INTENT_PHRASES = [
    "review",
    "check",
    "inspect",
    "analyze",
    "analyse",
    "look at",
    "look into",
    "see if",
    "find",
    "spot",
    "detect",
    "identify",
    "is there",
    "any issue",
    "any issues",
    "any error",
    "any errors",
    "problem",
    "problems",
    "bug",
    "bugs",
    "fix",
    "improve",
    "suggest",
]

CONTENT_HINT_PHRASES = [
    "code",
    "api",
    "error",
    "errors",
    "issue",
    "issues",
    "bug",
    "bugs",
    "design",
    "layout",
    "page",
    "website",
    "webpage",
    "ppt",
    "powerpoint",
    "summary",
    "summarize",
    "sql",
    "query",
    "architecture",
    "frontend",
    "backend",
    "devops",
    "quality",
    "testing",
    "bedrock",
]


def has_intent(normalized_query: str) -> bool:
    return contains_any(normalized_query, GENERAL_INTENT_PHRASES)


def has_content_hint(normalized_query: str) -> bool:
    return contains_any(normalized_query, CONTENT_HINT_PHRASES)


CONTACT_LINE_PATTERNS = [
    r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
    r"\b(?:\+?\d[\d\s().-]{7,}\d)\b",
    r"\blinkedin\b",
    r"\bgithub\b",
    r"\bportfolio\b",
    r"\bmailto:\b",
    r"\bhttps?://\S+",
    r"\bwww\.\S+",
]


def is_contact_or_metadata_line(line: str) -> bool:
    normalized_line = normalize_text(line)
    if not normalized_line:
        return True
    if any(re.search(pattern, line, re.IGNORECASE) for pattern in CONTACT_LINE_PATTERNS):
        return True
    metadata_markers = [
        "phone",
        "email",
        "linkedin",
        "github",
        "address",
        "contact",
        "resume",
        "curriculum vitae",
    ]
    return any(marker in normalized_line for marker in metadata_markers)


def collect_meaningful_lines(text: str) -> List[str]:
    lines: List[str] = []
    for raw_line in text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            continue
        if is_contact_or_metadata_line(stripped_line):
            continue
        if len(stripped_line) < 20 and not re.search(r"[.!?;:]", stripped_line):
            continue
        lines.append(stripped_line)
    return lines


def group_document_sections(lines: List[str]) -> List[List[str]]:
    sections: List[List[str]] = []
    current_section: List[str] = []

    for line in lines:
        colon_parts = line.split(":", 1)
        colon_heading = len(colon_parts) == 2 and len(colon_parts[0].split()) <= 4
        is_heading = (
            len(line) <= 60
            and (
                line.endswith(":")
                or line.isupper()
                or colon_heading
                or (len(line.split()) <= 6 and not re.search(r"[.!?]", line))
            )
        )

        if is_heading and current_section:
            sections.append(current_section)
            current_section = [line]
            continue

        if is_heading and not current_section:
            current_section.append(line)
            continue

        current_section.append(line)

    if current_section:
        sections.append(current_section)

    return sections


def build_summary_points(lines: List[str]) -> List[str]:
    if not lines:
        return []

    sections = group_document_sections(lines)
    key_points: List[str] = []

    for section in sections:
        heading = section[0]
        body_lines = [line for line in section[1:] if len(line) > 20 or re.search(r"[.!?]", line)]
        if body_lines:
            combined = f"{heading}: {' '.join(body_lines[:2])}" if heading != body_lines[0] else heading
        else:
            combined = heading

        if combined not in key_points:
            key_points.append(combined[:220])
        if len(key_points) >= 6:
            break

    if not key_points:
        key_points = [line[:220] for line in lines[:6]]

    return key_points


def get_allowed_skill_names() -> List[str]:
    return list(REGISTERED_MCP_SKILLS.keys())


def get_allowed_skill_descriptions() -> List[str]:
    return [
        "review_python_code: review Python code for style, logic, best practices, and bugs",
        "create_ppt: create PowerPoint slide outlines",
        "summarize_document: summarize documents and long-form text",
        "aws_cost_analyzer: analyze AWS costs and optimization opportunities",
        "sql_generator: generate or optimize SQL queries",
        "architecture_diagram_generator: create architecture diagram descriptions",
        "frontend_developer: review frontend UI, accessibility, performance, and compatibility",
        "devops_engineer: review deployment, automation, CI/CD, and infrastructure",
        "quality_engineer: assess testing, quality gates, validation, and reliability",
        "backend_developer: review backend architecture, APIs, security, and scalability",
        "bedrock_text_generator: generate text using AWS Bedrock models",
    ]


def looks_like_python_code(input_text: str) -> bool:
    python_patterns = [
        r"\bdef\s+\w+\s*\(",
        r"\bclass\s+\w+",
        r"\bimport\s+\w+",
        r"\bfrom\s+\w+\s+import\b",
        r"\bprint\s*\(",
        r"\binput\s*\(",
        r"\bif\s+.+:",
        r"\bfor\s+\w+\s+in\s+.+:",
        r"\bwhile\s+.+:",
        r"```python",
    ]
    return any(re.search(pattern, input_text, re.IGNORECASE) for pattern in python_patterns)


def looks_like_backend_code(input_text: str) -> bool:
    backend_patterns = [
        r"\bpublic\s+class\s+\w+",
        r"\bpublic\s+static\s+void\s+main\s*\(",
        r"\bimport\s+java\.",
        r"@RestController\b",
        r"@GetMapping\b",
        r"@PostMapping\b",
        r"ResponseEntity\s*<",
        r"require\s*\(\s*['\"]express['\"]\s*\)",
        r"\bexpress\s*\(",
        r"\bapp\.use\s*\(",
        r"\bapp\.listen\s*\(",
        r"\bapp\.(get|post|put|delete)\s*\(",
        r"\bapp\.(patch|all|route)\s*\(",
        r"\brouter\.(get|post|put|delete)\s*\(",
        r"\brouter\.(patch|all|route)\s*\(",
        r"\b(req|res)\s*=>",
        r"\b(req|res)\.",
        r"@app\.(get|post|put|delete)\s*\(",
        r"\bFastAPI\s*\(",
    ]
    return any(re.search(pattern, input_text, re.IGNORECASE) for pattern in backend_patterns)


def is_python_code_review_request(input_text: str) -> bool:
    normalized_query = normalize_text(input_text)
    return has_intent(normalized_query) and (
        "code" in normalized_query or looks_like_python_code(input_text)
    ) and looks_like_python_code(input_text)


def is_backend_review_request(input_text: str, normalized_query: str) -> bool:
    asks_for_review = has_intent(normalized_query)
    mentions_backend = contains_any(
        normalized_query,
        [
            "backend",
            "back end",
            "api",
            "server",
            "service",
            "java",
            "spring",
            "node",
            "express",
            "fastapi",
            "rest",
            "controller",
        ],
    )

    return asks_for_review and mentions_backend and (
        "code" in normalized_query
        or has_content_hint(normalized_query)
        or looks_like_backend_code(input_text)
    )


def is_create_ppt_request(normalized_query: str) -> bool:
    return has_intent(normalized_query) and contains_any(
        normalized_query,
        ["ppt", "powerpoint", "presentation", "slide", "slides"],
    )


def is_summarize_document_request(normalized_query: str) -> bool:
    return has_intent(normalized_query) and contains_any(
        normalized_query,
        ["summarize", "summary", "document summary", "summarization"],
    )


def is_aws_cost_request(normalized_query: str) -> bool:
    return has_intent(normalized_query) and contains_any(normalized_query, ["aws", "cloud"]) and contains_any(
        normalized_query,
        ["cost", "billing", "spend", "pricing", "optimization", "expense"],
    )


def is_sql_request(normalized_query: str) -> bool:
    return has_intent(normalized_query) and contains_any(
        normalized_query,
        ["sql", "query", "database query", "select", "insert", "update", "delete"],
    )


def is_architecture_diagram_request(normalized_query: str) -> bool:
    return has_intent(normalized_query) and contains_any(
        normalized_query,
        ["architecture", "diagram", "cloud design", "system design"],
    )


def is_engineering_review_request(normalized_query: str) -> bool:
    return has_intent(normalized_query) and contains_any(
        normalized_query,
        [
            "webpage",
            "website",
            "page design",
            "design quality",
            "ui design",
            "frontend",
            "front end",
            "ui",
            "ux",
            "layout",
            "styling",
            "typography",
            "responsive",
            "responsive design",
            "accessibility",
            "backend",
            "back end",
            "api",
            "server",
            "scalability",
            "devops",
            "ci/cd",
            "deployment",
            "infrastructure",
            "kubernetes",
            "docker",
            "quality",
            "qa",
            "testing",
            "test coverage",
            "validation",
        ],
    )


def is_bedrock_text_generation_request(normalized_query: str) -> bool:
    return has_intent(normalized_query) and contains_any(
        normalized_query,
        ["bedrock", "aws bedrock", "text generation", "llm"],
    )


def is_skill_related_question(input_text: str) -> bool:
    normalized_query = normalize_text(input_text)

    asks_for_registered_skills = any(
        request in normalized_query for request in REGISTERED_SKILL_LIST_REQUESTS
    )

    return (
        asks_for_registered_skills
        or is_python_code_review_request(input_text)
        or is_backend_review_request(input_text, normalized_query)
        or is_create_ppt_request(normalized_query)
        or is_summarize_document_request(normalized_query)
        or is_aws_cost_request(normalized_query)
        or is_sql_request(normalized_query)
        or is_architecture_diagram_request(normalized_query)
        or is_engineering_review_request(normalized_query)
        or is_bedrock_text_generation_request(normalized_query)
    )


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
    meaningful_lines = collect_meaningful_lines(text)
    source_lines = meaningful_lines or [p.strip() for p in text.split("\n\n") if p.strip()]
    key_points = build_summary_points(source_lines)
    if not key_points and text.strip():
        key_points = [text.strip()[:160]]
    return {
        "tool": "summarize_document",
        "summary": f"Document summary created from {len(source_lines)} meaningful lines.",
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
    normalized_input = input_text.lower()
    if "accessibility" not in normalized_input:
        issues.append("Check accessibility for keyboard navigation and screen readers.")
    if "performance" not in normalized_input:
        issues.append("Evaluate frontend performance, bundle size, and rendering speed.")
    if not any(term in normalized_input for term in ["design", "layout", "typography", "spacing", "responsive"]):
        issues.append("Review visual hierarchy, spacing, and responsive behavior.")
    if not any(term in normalized_input for term in ["error", "issue", "bug", "problem", "interaction"]):
        issues.append("Check for broken interactions, button states, and feedback messages.")
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
    """Call AWS Bedrock text generation using the Converse API (works with Claude, Nova, etc)."""
    model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-pro-v1:0")
    region = os.getenv("AWS_REGION", "us-east-1")
    try:
        client = boto3.client("bedrock-runtime", region_name=region)
        # Use Converse API for universal model support
        response = client.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ],
            inferenceConfig={
                "maxTokens": 1024,
                "temperature": 0.7
            }
        )
        # Extract text from response
        generated_text = response["output"]["message"]["content"][0]["text"]
        return {
            "tool": "bedrock_text_generator",
            "model_id": model_id,
            "response": generated_text,
        }
    except (BotoCoreError, ClientError) as exc:
        return {
            "tool": "bedrock_text_generator",
            "error": "Bedrock call failed.",
            "details": str(exc),
        }


def get_local_agent_response(input_text: str) -> str:
    normalized_query = normalize_text(input_text)

    if is_backend_review_request(input_text, normalized_query):
        result = backend_developer(input_text)
        suggestions = "\n".join(f"- {suggestion}" for suggestion in result["suggestions"])
        return f"{result['summary']}\n\n{suggestions}"

    if is_python_code_review_request(input_text):
        result = review_python_code(input_text)
        issues = "\n".join(f"- {issue}" for issue in result["issues"])
        return f"{result['summary']}\n\n{issues}"

    if is_create_ppt_request(normalized_query):
        result = create_ppt(input_text)
        slides = "\n".join(
            f"- {slide['title']}: {slide['content']}" for slide in result["slides"]
        )
        return f"{result['summary']}\n\n{slides}"

    if is_summarize_document_request(normalized_query):
        result = summarize_document(input_text)
        points = "\n".join(f"- {point}" for point in result["key_points"])
        return f"{result['summary']}\n\n{points}\n\n{result['recommendation']}"

    if is_aws_cost_request(normalized_query):
        result = aws_cost_analyzer(input_text)
        insights = "\n".join(f"- {insight}" for insight in result["insights"])
        return f"{result['summary']}\n\n{insights}"

    if is_sql_request(normalized_query):
        result = sql_generator(input_text)
        notes = "\n".join(f"- {note}" for note in result["notes"])
        return f"{result['summary']}\n\n{result['query']}\n\n{notes}"

    if is_architecture_diagram_request(normalized_query):
        result = architecture_diagram_generator(input_text)
        steps = "\n".join(f"- {step}" for step in result["diagram_steps"])
        return f"{result['summary']}\n\n{steps}\n\n{result['recommendation']}"

    if contains_any(normalized_query, ["frontend", "front end", "ui", "ux", "accessibility"]):
        result = frontend_developer(input_text)
        recommendations = "\n".join(
            f"- {recommendation}" for recommendation in result["recommendations"]
        )
        return f"{result['summary']}\n\n{recommendations}"

    if contains_any(normalized_query, ["devops", "ci/cd", "deployment", "infrastructure", "kubernetes", "docker"]):
        result = devops_engineer(input_text)
        recommendations = "\n".join(
            f"- {recommendation}" for recommendation in result["recommendations"]
        )
        return f"{result['summary']}\n\n{recommendations}"

    if contains_any(normalized_query, ["quality", "qa", "testing", "test coverage", "validation"]):
        result = quality_engineer(input_text)
        observations = "\n".join(
            f"- {observation}" for observation in result["observations"]
        )
        return f"{result['summary']}\n\n{observations}"

    return (
        "This question is allowed because it matches a registered MCP skill. "
        f"Registered skills: {', '.join(get_allowed_skill_names())}"
    )


def assistant_agent(input_text: str) -> Dict[str, Any]:
    """A simple agent tool that either forwards to Bedrock or returns a conversational response."""
    allowed_skills = get_allowed_skill_names()

    if not is_skill_related_question(input_text):
        return {
            "tool": "assistant_agent",
            "summary": "Rejected by skills-topic guardrail.",
            "assistant_response": SKILL_GUARDRAIL_MESSAGE,
            "guardrail": {
                "allowed": False,
                "reason": "Input is outside the skills-related scope.",
            },
        }

    if os.getenv("BEDROCK_ENABLED", "true").lower() in ("true", "1", "yes"):
        allowed_skills_text = "\n".join(
            f"- {skill}" for skill in get_allowed_skill_descriptions()
        )
        prompt = (
            "You are a skills analysis assistant. Only answer questions about the "
            "registered MCP skills listed below. Do not answer questions about skills, "
            "topics, tools, technologies, or general knowledge outside this registered list.\n\n"
            f"Registered MCP skills:\n{allowed_skills_text}\n\n"
            "If the user provides Python-looking code and asks to review, check, fix, "
            "improve, debug, or analyze it, that is within the review_python_code skill.\n\n"
            "If the user provides Java, Spring, Node, Express, FastAPI, API, or server code "
            "and asks for backend review, that is within the backend_developer skill. "
            "Review the code instead of refusing it.\n\n"
            "Do not treat a plain sentence followed by 'review this' as Python code review "
            "unless the input includes Python-looking code.\n\n"
            "If the user asks for anything outside that scope, respond only with: "
            f"{SKILL_GUARDRAIL_MESSAGE}\n\n"
            "User input:\n"
            + input_text
        )
        bedrock_result = bedrock_text_generator(prompt)
        if bedrock_result.get("response"):
            return {
                "tool": "assistant_agent",
                "summary": "Bedrock-powered assistant response.",
                "assistant_response": bedrock_result["response"],
            }
        return {
            "tool": "assistant_agent",
            "summary": "Local fallback assistant response after Bedrock failure.",
            "assistant_response": get_local_agent_response(input_text),
            "details": bedrock_result.get("details"),
        }
    return {
        "tool": "assistant_agent",
        "summary": "Local fallback assistant response.",
        "assistant_response": get_local_agent_response(input_text),
    }
