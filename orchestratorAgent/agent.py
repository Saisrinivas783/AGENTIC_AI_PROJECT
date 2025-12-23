from typing import Dict, Any

from schemas.api import InvocationRequest, InvocationResponse
from schemas.state import OrchestratorState
from registry.loader import load_tools_registry
from orchestrator.graph import build_graph


class OrchestratorAgent:
    def __init__(self, registry_path: str = "registry/tools-config.yaml"):
        self.registry_path = registry_path
        self.registry = load_tools_registry(self.registry_path)
        self.graph_app = build_graph(self.registry)

    def handle_invocation(self, payload: InvocationRequest) -> InvocationResponse:
        state = OrchestratorState(
            query=payload.userPrompt,
            session_id=payload.sessionId,
            context=payload.context.model_dump() if payload.context else {},
        )

        out_dict: Dict[str, Any] = self.graph_app.invoke(state.model_dump())
        out_state = OrchestratorState(**out_dict)

        overall_conf = 0.0
        if out_state.selected_tools:
            overall_conf = float(max(t.confidence for t in out_state.selected_tools))

        return InvocationResponse(
            sessionId=payload.sessionId,
            selectedTool=out_state.selected_tools,
            confidence=overall_conf,
            responseText=out_state.tool_results,
        )
