import json

from app.browser.crawler import crawl_domain
from app.extraction.business_analyzer import (
    analyze_business_metrics,
    load_business_metrics,
)
from app.extraction.enrichment import enrich_company
from app.extraction.preprocessor import prepare_context
from app.llm.business_analyzer import analyze_business
from app.llm.extractor import extract_company_intelligence_with_usage
from app.observability.evidence import build_evidence
from app.observability.metrics import Timer
from app.observability.quality import (
    build_quality_flags,
    calculate_quality_score,
)
from app.resilience.retry import retry


DOMAINS = [
    "postman.com",
    "supabase.com",
    "vapi.ai",
]


def process_domain(domain: str, business_row: dict) -> dict:
    timer = Timer()

    try:
        with timer:

            def run():
                crawl_result = crawl_domain(domain)

                pages = crawl_result["pages"]
                crawl_errors = crawl_result["errors"]

                context = prepare_context(pages)

                intelligence, usage = extract_company_intelligence_with_usage(context)
                intelligence_data = intelligence.model_dump()

                company_name = str(business_row["company"])

                enrichment = enrich_company(
                    domain,
                    company_name,
                )

                calculated_metrics = analyze_business_metrics(
                    business_row
                )

                business_analysis = analyze_business(
                    intelligence_data,
                    business_row,
                    calculated_metrics,
                )

                quality_score = calculate_quality_score(
                    intelligence,
                    len(pages),
                    crawl_errors,
                )

                quality_flags = build_quality_flags(
                    intelligence,
                    crawl_errors,
                )

                evidence = build_evidence(pages)

                return {
                    "domain": domain,
                    "status": "success",
                    "pages_collected": len(pages),

                    "intelligence": intelligence_data,
                    "usage": usage,

                    "business_metrics": business_row,

                    "calculated_metrics": calculated_metrics,

                    "business_analysis": business_analysis.model_dump(),

                    "enrichment": enrichment,

                    "quality_score": quality_score,
                    "quality_flags": quality_flags,

                    "evidence": evidence,
                    "crawl_errors": crawl_errors,
                }

            result = retry(
                run,
                attempts=2,
                delay_seconds=1,
            )

        result["execution_time_seconds"] = round(
            timer.elapsed_seconds,
            2,
        )

        return result

    except Exception as exc:
        return {
            "domain": domain,
            "status": "failed",
            "error": str(exc),
            "execution_time_seconds": round(
                timer.elapsed_seconds,
                2,
            ),
        }


def main() -> None:
    business_df = load_business_metrics()

    results = []

    for domain in DOMAINS:
        company_name = domain.split(".")[0]

        matches = business_df[
            business_df["company"].str.lower()
            == company_name.lower()
        ]

        if matches.empty:
            print(
                f"\nSkipping {domain}: "
                "no business data found"
            )
            continue

        business_row = matches.iloc[0].to_dict()

        print(f"\nProcessing {domain}...")

        result = process_domain(
            domain,
            business_row,
        )

        if result["status"] == "success":
            print("  ✓ Crawl complete")
            print("  ✓ LLM extraction complete")
            print("  ✓ Business KPI analysis complete")
            print("  ✓ Search enrichment complete")
            print(
                f"  ✓ Search sources: "
                f"{result['enrichment']['search_sources']}"
            )
            print(
                f"  ✓ LinkedIn sources: "
                f"{result['enrichment']['linkedin_sources']}"
            )
            print(
                f"  ✓ Opportunity score: "
                f"{result['calculated_metrics']['opportunity_score']}/100"
            )
            print(
                f"  ✓ Strategic fit: "
                f"{result['business_analysis']['strategic_fit_score']:.2f}"
            )
            print(
                f"  ✓ Evidence sources: "
                f"{len(result['evidence'])}"
            )
        else:
            print(
                f"  ✗ Failed: {result['error']}"
            )

        print(
            f"  Time: "
            f"{result['execution_time_seconds']} seconds"
        )

        results.append(result)

    with open(
        "output/output.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=2,
            ensure_ascii=False,
        )

    successful = sum(
        result["status"] == "success"
        for result in results
    )

    print(
        f"\nCompleted: "
        f"{successful}/{len(results)} domains successfully"
    )

    print("Saved: output/output.json")


if __name__ == "__main__":
    main()
