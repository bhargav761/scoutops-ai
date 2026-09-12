def calculate_quality_score(intelligence, pages_count: int, crawl_errors: list) -> float:
    score = 0.0

    if intelligence.company_overview.strip():
        score += 0.20

    if intelligence.target_audience.strip():
        score += 0.20

    if intelligence.contact_points:
        score += 0.15

    if intelligence.leadership:
        score += 0.15

    if pages_count >= 3:
        score += 0.15
    elif pages_count >= 1:
        score += 0.08

    if not crawl_errors:
        score += 0.15

    return round(min(score, 1.0), 2)


def build_quality_flags(intelligence, crawl_errors: list) -> list[str]:
    flags = []

    if not intelligence.company_overview.strip():
        flags.append("missing_company_overview")

    if not intelligence.target_audience.strip():
        flags.append("missing_target_audience")

    if not intelligence.contact_points:
        flags.append("no_public_contact_email")

    if not intelligence.leadership:
        flags.append("leadership_not_found")

    if crawl_errors:
        flags.append("crawl_errors_detected")

    if intelligence.confidence_score < 0.70:
        flags.append("low_llm_confidence")

    return flags
