from pydantic import BaseModel, Field


class BusinessAnalysis(BaseModel):
    growth_assessment: str
    risk_assessment: str
    opportunity_assessment: str
    recommended_action: str
    strategic_fit_score: float = Field(ge=0.0, le=1.0)
