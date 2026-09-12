from google import genai

from app.config import GEMINI_API_KEY, LLM_MODEL
from app.llm.schema import CompanyIntelligence
from app.observability.cost import build_usage_metrics


SYSTEM_PROMPT = """
You are a company intelligence extraction agent.

Analyze the supplied public website content and return structured company
intelligence.

Rules:
- Do not invent facts.
- Use only information supported by the supplied content.
- Company overview should be concise, approximately two sentences.
- Identify the likely target audience / ICP.
- Include only generic or public contact emails actually found.
- Extract leadership/team members only when supported by the content.
- Include LinkedIn URLs only when actually present.
- Confidence score must be between 0.0 and 1.0.
"""


def extract_company_intelligence_with_usage(
    context: str,
) -> tuple[CompanyIntelligence, dict]:

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Add it to .env."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=f"{SYSTEM_PROMPT}\n\nWebsite content:\n{context}",
        config={
            "response_mime_type": "application/json",
            "response_schema": CompanyIntelligence,
        },
    )

    usage = getattr(response, "usage_metadata", None)

    input_tokens = getattr(
        usage,
        "prompt_token_count",
        0,
    ) if usage else 0

    output_tokens = getattr(
        usage,
        "candidates_token_count",
        0,
    ) if usage else 0

    metrics = build_usage_metrics(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )

    return (
        CompanyIntelligence.model_validate_json(response.text),
        {
            "input_tokens": metrics.input_tokens,
            "output_tokens": metrics.output_tokens,
            "total_tokens": metrics.total_tokens,
            "estimated_cost_usd": metrics.estimated_cost_usd,
        },
    )


def extract_company_intelligence(
    context: str,
) -> CompanyIntelligence:

    intelligence, _ = extract_company_intelligence_with_usage(context)

    return intelligence
