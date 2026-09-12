from google import genai

from app.config import GEMINI_API_KEY, LLM_MODEL
from app.llm.business_schema import BusinessAnalysis


PROMPT = """
You are a senior business intelligence analyst.

Analyze the company intelligence and business KPI data.

Rules:
- Use only supplied information.
- Do not invent financial facts.
- Explain the growth situation.
- Identify important business risks.
- Identify the strongest opportunity.
- Recommend one practical action.
- Strategic fit score must be between 0 and 1.
"""


def analyze_business(
    company_intelligence: dict,
    business_metrics: dict,
    calculated_metrics: dict,
) -> BusinessAnalysis:

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    content = f"""
{PROMPT}

COMPANY INTELLIGENCE:
{company_intelligence}

BUSINESS METRICS:
{business_metrics}

CALCULATED KPI SIGNALS:
{calculated_metrics}
"""

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=content,
        config={
            "response_mime_type": "application/json",
            "response_schema": BusinessAnalysis,
        },
    )

    return BusinessAnalysis.model_validate_json(response.text)
