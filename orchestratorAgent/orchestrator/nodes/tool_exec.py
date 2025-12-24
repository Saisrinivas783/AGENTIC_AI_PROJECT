from schemas.state import OrchestratorState


def tool_exec_node(state: OrchestratorState) -> OrchestratorState:
    state.tool_results = []
    return state
