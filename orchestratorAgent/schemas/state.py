from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    tool_name: str
    reason: str
    confidence: float
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    tool_name: str
    ok: bool
    raw_response: Any = None
    error: Optional[str] = None


class OrchestratorState(BaseModel):
    query: str
    session_id: str
    context: Dict[str, Any] = Field(default_factory=dict)

    intent: Optional[str] = None
    intent_confidence: Optional[float] = None

    selected_tool_candidates: List[str] = Field(default_factory=list)

    selected_tools: List[ToolCall] = Field(default_factory=list)

    tool_results: List[ToolResult] = Field(default_factory=list)

    final_answer: Optional[str] = None
    selected_tool_name: Optional[str] = None
    selected_tool_confidence: Optional[float] = None

    messages: List[str] = Field(default_factory=list)
