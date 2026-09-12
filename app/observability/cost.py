from dataclasses import dataclass


# Approximate Gemini pricing configuration.
# Keep these configurable so pricing can be updated without changing code.
INPUT_COST_PER_1M = 0.30
OUTPUT_COST_PER_1M = 2.50


@dataclass
class UsageMetrics:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
) -> float:
    input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_1M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M

    return round(input_cost + output_cost, 6)


def build_usage_metrics(
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> UsageMetrics:
    total_tokens = input_tokens + output_tokens

    return UsageMetrics(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=calculate_cost(
            input_tokens,
            output_tokens,
        ),
    )
