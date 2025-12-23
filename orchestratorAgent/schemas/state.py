from typing import List, Optional
from pydantic import BaseModel, Field
from schemas.api import InvocationContext
from .tools import SelectedTools, ToolResult


class OrchestratorState(BaseModel):
    query: str
    session_id: str

    context: Optional[InvocationContext] = None

    intent: Optional[str] = None
    intent_confidence: Optional[float] = None

    selected_tools: List[SelectedTools] = Field(default_factory=list)

    tool_results: List[ToolResult] = Field(default_factory=list)

    final_answer: Optional[str] = None
