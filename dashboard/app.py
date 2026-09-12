import json
from pathlib import Path

import streamlit as st


OUTPUT_FILE = Path("output/output.json")


st.set_page_config(
    page_title="ScoutOps AI",
    page_icon="🎯",
    layout="wide",
)


@st.cache_data
def load_results():
    if not OUTPUT_FILE.exists():
        return []

    with OUTPUT_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


results = load_results()

st.title("🎯 ScoutOps AI")
st.caption("AI-Powered Company Intelligence & Business Opportunity Platform")

if not results:
    st.warning("No analysis results found. Run the pipeline first.")
    st.stop()


successful = [
    item for item in results
    if item.get("status") == "success"
]

# -----------------------------
# Executive metrics
# -----------------------------

st.subheader("Executive Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Companies", len(results))

with col2:
    st.metric("Successful", len(successful))

with col3:
    scores = [
        item.get("quality_score", 0)
        for item in successful
    ]
    avg_quality = (
        sum(scores) / len(scores)
        if scores else 0
    )
    st.metric("Avg Quality", f"{avg_quality:.2f}")

with col4:
    opportunity_scores = [
        item.get("business_analysis", {})
        .get("opportunity_score", 0)
        for item in successful
    ]
    avg_opportunity = (
        sum(opportunity_scores) / len(opportunity_scores)
        if opportunity_scores else 0
    )
    st.metric("Avg Opportunity", f"{avg_opportunity:.0f}/100")

with col5:
    total_cost = sum(
        item.get("usage", {})
        .get("estimated_cost_usd", 0)
        for item in successful
    )
    st.metric("Est. LLM Cost", f"${total_cost:.4f}")


st.divider()

# -----------------------------
# Company selector
# -----------------------------

domains = [
    item.get("domain", "unknown")
    for item in results
]

selected_domain = st.selectbox(
    "Select company",
    domains,
)

company = next(
    item for item in results
    if item.get("domain") == selected_domain
)

intelligence = company.get("intelligence", {})
business = company.get("business_analysis", {})
calculated = company.get("calculated_metrics", {})
enrichment = company.get("enrichment", {})
usage = company.get("usage", {})

# -----------------------------
# Company intelligence
# -----------------------------

st.header(f"🏢 {selected_domain}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Company Intelligence")

    st.write(
        intelligence.get(
            "company_overview",
            "No overview available.",
        )
    )

    st.markdown(
        f"**Target Audience:** "
        f"{intelligence.get('target_audience', 'N/A')}"
    )

with col2:
    st.subheader("Leadership")

    leadership = intelligence.get("leadership", [])

    if leadership:
        for person in leadership:
            st.write(
                f"**{person.get('name', 'Unknown')}** — "
                f"{person.get('role', 'Unknown role')}"
            )

            if person.get("linkedin_url"):
                st.write(person["linkedin_url"])
    else:
        st.info("No leadership data found.")


# -----------------------------
# Business intelligence
# -----------------------------

st.divider()
st.header("📊 Business Intelligence")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Opportunity",
        f"{business.get('opportunity_score', 0)}/100",
    )

with col2:
    st.metric(
        "Strategic Fit",
        f"{business.get('strategic_fit_score', 0):.2f}",
    )

with col3:
    st.metric(
        "LTV / CAC",
        calculated.get("ltv_cac_ratio", "N/A"),
    )

with col4:
    st.metric(
        "Growth",
        calculated.get("growth_signal", "N/A"),
    )

with col5:
    st.metric(
        "Retention",
        calculated.get("retention_signal", "N/A"),
    )

st.subheader("Business Recommendation")

recommendation = business.get(
    "recommendation",
    "No recommendation available.",
)

st.info(recommendation)


# -----------------------------
# Evidence & discovery
# -----------------------------

st.divider()
st.header("🔎 Evidence & Discovery")

col1, col2, col3 = st.columns(3)

with col1:
    evidence = company.get("evidence", [])
    st.metric("Evidence Sources", len(evidence))

with col2:
    st.metric(
        "Search Sources",
        enrichment.get("search_sources", 0),
    )

with col3:
    st.metric(
        "LinkedIn Sources",
        enrichment.get("linkedin_sources", 0),
    )

with st.expander("Evidence Sources"):
    for source in evidence:
        st.write(
            f"🔗 {source.get('source_url', 'N/A')}"
        )


with st.expander("Search Results"):
    for result in enrichment.get("search_results", []):
        st.markdown(
            f"**{result.get('title', 'Untitled')}**"
        )
        st.write(result.get("snippet", ""))
        st.write(result.get("url", ""))
        st.divider()


with st.expander("LinkedIn Discovery"):
    for result in enrichment.get("linkedin_results", []):
        st.markdown(
            f"**{result.get('title', 'Untitled')}**"
        )
        st.write(result.get("url", ""))
        st.write(result.get("snippet", ""))
        st.divider()


# -----------------------------
# Quality & observability
# -----------------------------

st.divider()
st.header("🛡️ Quality & Run Observability")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Quality Score",
        f"{company.get('quality_score', 0):.2f}",
    )

with col2:
    st.metric(
        "Pages",
        company.get("pages_collected", 0),
    )

with col3:
    st.metric(
        "Execution",
        f"{company.get('execution_time_seconds', 0):.2f}s",
    )

with col4:
    st.metric(
        "Confidence",
        f"{intelligence.get('confidence_score', 0) * 100:.0f}%",
    )


flags = company.get("quality_flags", [])

if flags:
    st.warning("Quality flags detected")
    for flag in flags:
        st.write(f"⚠️ {flag}")
else:
    st.success("No quality flags")


# -----------------------------
# LLM usage
# -----------------------------

st.subheader("🧠 LLM Usage & Cost")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Input Tokens",
        usage.get("input_tokens", 0),
    )

with col2:
    st.metric(
        "Output Tokens",
        usage.get("output_tokens", 0),
    )

with col3:
    st.metric(
        "Total Tokens",
        usage.get("total_tokens", 0),
    )

with col4:
    st.metric(
        "Estimated Cost",
        f"${usage.get('estimated_cost_usd', 0):.6f}",
    )


# -----------------------------
# Run information
# -----------------------------

if company.get("run_id"):
    st.subheader("Run Information")

    st.code(
        company["run_id"],
        language="text",
    )
