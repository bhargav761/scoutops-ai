from google import genai

from app.config import GEMINI_API_KEY, LLM_MODEL
from app.llm.schema import CompanyIntelligence


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


def extract_company_intelligence(context: str) -> CompanyIntelligence:
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

    return CompanyIntelligence.model_validate_json(response.text)
