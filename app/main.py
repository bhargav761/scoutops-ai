import json

from app.browser.crawler import crawl_domain


def main() -> None:
    domains = [
        "postman.com",
    ]

    for domain in domains:
        print(f"\nCrawling {domain}...")

        result = crawl_domain(domain)

        print(f"Pages collected: {len(result['pages'])}")
        print(f"Errors: {len(result['errors'])}")

        with open("output/crawl.json", "w", encoding="utf-8") as file:
            json.dump(result, file, indent=2, ensure_ascii=False)

        print("Saved: output/crawl.json")


if __name__ == "__main__":
    main()
