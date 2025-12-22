import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

print("OPENAI_API_KEY loaded:", bool(os.getenv("OPENAI_API_KEY")))

def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip().strip('"').strip("'")

def make_llm(model: str = "gpt-4o-mini", temperature: float = 0.15):
    api_key = _clean(os.getenv("OPENAI_API_KEY"))
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY not found. Fix .env formatting OR export OPENAI_API_KEY before running uvicorn."
        )

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=temperature,
    )
    

if __name__ == "__main__":
    llm = make_llm()
    print(llm.invoke("Hi").content)
