from app.browser.search import discover_linkedin, search_company


def enrich_company(domain: str, company_name: str) -> dict:
    search_results = search_company(
        domain,
        company_name,
        max_results=5,
    )

    linkedin_results = discover_linkedin(
        domain,
        company_name,
        max_results=5,
    )

    return {
        "search_results": search_results,
        "linkedin_results": linkedin_results,
        "search_sources": len(search_results),
        "linkedin_sources": len(linkedin_results),
    }
