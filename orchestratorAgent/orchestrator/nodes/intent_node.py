import json
from schemas.state import OrchestratorState
from pydantic import BaseModel, Field

from llm.bedrock_llm_client import make_llm


class IntentFormat(BaseModel):
    intent: str = Field(description="Short intent label, e.g., benefits_coverage, claims, provider_search, general")
    intent_confidence: float = Field(description="Confidence score between 0 and 1 indicating the certainty of the intent")
    reason: str = Field(description="Explanation for the intent classification")


SYSTEM_PROMPT = """
You are an intent classification model.

Classify the user's query into ONE of the following intents:
- benefits_coverage
- claims
- provider_search
- eligibility
- billing_payments
- general

Return ONLY valid JSON in this format:
{
  "intent": "<intent>",
  "intent_confidence": <float between 0 and 1>,
  "reason": "<short explanation>"
}
"""


def extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output")
    return text[start : end + 1]


def intent_node(state: OrchestratorState) -> OrchestratorState:
    user_query = state.query

    llm = make_llm(
        model="openai.gpt-oss-20b-1:0",
        region="us-east-1",
        temperature=0.0,
    )

    response = llm.invoke(
        user_text=user_query,
        system_text=SYSTEM_PROMPT,
    )

    raw = response.raw
    json_text = raw["choices"][0]["message"]["content"]
    json_text = extract_json(json_text)

    parsed = IntentFormat.model_validate_json(json_text)

    # 🔽 DEBUG
    print("\n========== INTENT NODE DEBUG (BEDROCK) ==========")
    print("User Query:", user_query)
    print("Raw Model Output:", raw)
    print("Extracted JSON:", json_text)
    print("Detected Intent:", parsed.intent)
    print("Intent Confidence:", parsed.intent_confidence)
    print("Intent Reason:", parsed.reason)
    print("===============================================\n")

    state.intent = parsed.intent
    state.intent_confidence = float(parsed.intent_confidence)

    return state
