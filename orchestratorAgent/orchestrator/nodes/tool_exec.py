from schemas.state import OrchestratorState


def tool_exec_node(state: OrchestratorState, registry: dict) -> OrchestratorState:
    state.tool_results = []
    return state
