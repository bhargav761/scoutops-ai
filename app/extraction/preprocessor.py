import re

from app.config import MAX_CONTENT_TOKENS


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def prepare_context(pages: list[dict]) -> str:
    sections = []

    for page in pages:
        text = clean_text(page.get("text", ""))

        if not text:
            continue

        sections.append(
            f"URL: {page.get('url', '')}\n"
            f"TITLE: {page.get('title', '')}\n"
            f"CONTENT:\n{text}"
        )

    context = "\n\n--- PAGE ---\n\n".join(sections)

    # Simple character-level budget to keep the first implementation
    # predictable and inexpensive.
    max_chars = MAX_CONTENT_TOKENS * 4

    return context[:max_chars]
