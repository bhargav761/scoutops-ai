from urllib.parse import urljoin, urlparse

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from app.config import MAX_PAGES_PER_DOMAIN, REQUEST_TIMEOUT_MS


IMPORTANT_PATHS = (
    "about",
    "team",
    "company",
    "contact",
    "pricing",
    "customers",
    "careers",
)


def normalize_domain(domain: str) -> str:
    domain = domain.strip()

    if not domain.startswith(("http://", "https://")):
        domain = f"https://{domain}"

    return domain.rstrip("/")


def is_internal(url: str, domain: str) -> bool:
    return urlparse(url).netloc == urlparse(domain).netloc


def clean_text(page) -> str:
    return page.locator("body").inner_text().strip()


def discover_links(page, domain: str) -> list[str]:
    links = []

    for link in page.locator("a").all():
        try:
            href = link.get_attribute("href")

            if not href:
                continue

            absolute = urljoin(domain, href)
            parsed = urlparse(absolute)

            if parsed.scheme not in ("http", "https"):
                continue

            absolute = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

            if is_internal(absolute, domain):
                links.append(absolute)

        except Exception:
            continue

    def priority(url: str) -> int:
        path = urlparse(url).path.lower()

        for index, name in enumerate(IMPORTANT_PATHS):
            if name in path:
                return index

        return len(IMPORTANT_PATHS)

    links.sort(key=priority)

    return list(dict.fromkeys(links))


def crawl_domain(domain: str) -> dict:
    domain = normalize_domain(domain)

    result = {
        "domain": urlparse(domain).netloc,
        "pages": [],
        "errors": [],
    }

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(
                domain,
                wait_until="domcontentloaded",
                timeout=REQUEST_TIMEOUT_MS,
            )

            page.wait_for_timeout(1000)

            homepage_text = clean_text(page)
            links = discover_links(page, domain)

            result["pages"].append(
                {
                    "url": page.url,
                    "title": page.title(),
                    "text": homepage_text,
                }
            )

            visited = {page.url}

            for url in links:
                if len(result["pages"]) >= MAX_PAGES_PER_DOMAIN:
                    break

                if url in visited:
                    continue

                visited.add(url)

                try:
                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=REQUEST_TIMEOUT_MS,
                    )

                    page.wait_for_timeout(500)

                    text = clean_text(page)

                    if text:
                        result["pages"].append(
                            {
                                "url": page.url,
                                "title": page.title(),
                                "text": text,
                            }
                        )

                except PlaywrightTimeoutError:
                    result["errors"].append(
                        {
                            "url": url,
                            "error": "timeout",
                        }
                    )

                except Exception as exc:
                    result["errors"].append(
                        {
                            "url": url,
                            "error": str(exc),
                        }
                    )

        except PlaywrightTimeoutError:
            result["errors"].append(
                {
                    "url": domain,
                    "error": "homepage timeout",
                }
            )

        except Exception as exc:
            result["errors"].append(
                {
                    "url": domain,
                    "error": str(exc),
                }
            )

        finally:
            browser.close()

    return result
