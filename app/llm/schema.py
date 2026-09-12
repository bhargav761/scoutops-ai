from pydantic import BaseModel, Field


class LeadershipMember(BaseModel):
    name: str
    role: str
    linkedin_url: str | None = None


class CompanyIntelligence(BaseModel):
    company_overview: str
    target_audience: str
    contact_points: list[str] = Field(default_factory=list)
    leadership: list[LeadershipMember] = Field(default_factory=list)
    confidence_score: float = Field(ge=0.0, le=1.0)
