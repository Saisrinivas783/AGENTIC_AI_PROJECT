import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class LLMResponse:
    """Match the minimal interface you use today: .content"""
    content: str
    raw: Dict[str, Any]


class BedrockChatLLM:
    """
    Tiny wrapper that feels like LangChain's Chat model:
      - llm = make_llm(...)
      - res = llm.invoke("hi")
      - print(res.content)
    """

    def __init__(
        self,
        model_id: str,
        region: str,
        temperature: float = 0.0,
        max_tokens: int = 300,
        profile_name: Optional[str] = None,
    ):
        self.model_id = model_id
        self.region = region
        self.temperature = float(temperature)
        self.max_tokens = int(max_tokens)

        # Uses your `aws configure` credentials by default.
        # If you want a named profile: profile_name="myprofile"
        if profile_name:
            session = boto3.Session(profile_name=profile_name, region_name=region)
        else:
            session = boto3.Session(region_name=region)

        self.client = session.client("bedrock-runtime")

    def invoke(self, user_text: str, system_text: Optional[str] = None) -> LLMResponse:
        messages = []
        if system_text:
            messages.append({"role": "system", "content": system_text})
        messages.append({"role": "user", "content": user_text})

        body = {
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        resp = self.client.invoke_model(
            modelId=self.model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )

        raw_str = resp["body"].read().decode("utf-8")
        raw = json.loads(raw_str)

        # Bedrock model providers return slightly different shapes.
        # Try a few common patterns to extract assistant text.
        text = (
            _try_get(raw, ["output", "message", "content", 0, "text"])  # common "chat" shape
            or _try_get(raw, ["content", 0, "text"])                   # another common shape
            or _try_get(raw, ["generation"])                           # some models
            or _try_get(raw, ["outputText"])                            # some models
        )

        if not isinstance(text, str):
            text = raw_str  # fallback: return the whole raw response as content

        return LLMResponse(content=text, raw=raw)


def _try_get(obj: Any, path: list) -> Any:
    cur = obj
    try:
        for p in path:
            if isinstance(p, int):
                cur = cur[p]
            else:
                cur = cur.get(p)
        return cur
    except Exception:
        return None


def make_llm(
    model: str = "openai.gpt-oss-20b-1:0",
    region: str = "us-east-1",
    temperature: float = 0.0,
    max_tokens: int = 300,
    profile_name: Optional[str] = None,
) -> BedrockChatLLM:
    return BedrockChatLLM(
        model_id=model,
        region=region,
        temperature=temperature,
        max_tokens=max_tokens,
        profile_name=profile_name,
    )


if __name__ == "__main__":
    llm = make_llm(region="us-east-1")
    res = llm.invoke("Say hello in French.")
    print(res.content)
