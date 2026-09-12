def build_evidence(pages: list[dict]) -> list[dict]:
    evidence = []

    for page in pages:
        url = page.get("url")

        if not url:
            continue

        text = page.get("text", "").strip()

        if not text:
            continue

        evidence.append(
            {
                "source_url": url,
                "source_type": "company_website",
                "content_length": len(text),
            }
        )

    return evidence
