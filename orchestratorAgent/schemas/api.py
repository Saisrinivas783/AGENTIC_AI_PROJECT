from typing import Any, Dict, Optional
from pydantic import BaseModel

class InvocationContext(BaseModel):
    userName: Optional[str] = None
    userType: Optional[str] = None
    source: Optional[str] = None
    promptId: Optional[str] = None

class InvocationRequest(BaseModel):
    userPrompt: str
    sessionId: str
    context: Optional[InvocationContext] = None

class InvocationResponse(BaseModel):
    sessionId: str
    selectedTool: str
    confidence: float
    responseText: str
    metadata: Dict[str, Any] = {}
