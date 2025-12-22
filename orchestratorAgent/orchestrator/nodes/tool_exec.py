from schemas.state import OrchestratorState

def tool_exec_node(state: OrchestratorState, registry: dict) -> OrchestratorState:
    state.tool_results = []
    state.messages.append("STUB tool_exec: cleared tool_results")
    return state
