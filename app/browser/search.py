from ddgs import DDGS


def search_company(domain: str, company_name: str, max_results: int = 5) -> list[dict]:
    query = f'"{company_name}" {domain} company leadership'

    results = []

    try:
        with DDGS() as ddgs:
            for result in ddgs.text(
                query,
                max_results=max_results,
            ):
                results.append(
                    {
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                    }
                )
    except Exception as exc:
        print(f"  Search warning: {exc}")

    return results


def discover_linkedin(
    domain: str,
    company_name: str,
    max_results: int = 5,
) -> list[dict]:
    query = f'site:linkedin.com/in "{company_name}" {domain}'

    results = []

    try:
        with DDGS() as ddgs:
            for result in ddgs.text(
                query,
                max_results=max_results,
            ):
                url = result.get("href", "")

                if "linkedin.com/in/" in url:
                    results.append(
                        {
                            "title": result.get("title", ""),
                            "url": url,
                            "snippet": result.get("body", ""),
                        }
                    )
    except Exception as exc:
        print(f"  LinkedIn search warning: {exc}")

    return results
