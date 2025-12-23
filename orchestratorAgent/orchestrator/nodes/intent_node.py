from schemas.state import OrchestratorState

def intent_node(state: OrchestratorState, registry: dict) -> OrchestratorState:
    state.intent = "benefits_coverage"
    state.intent_confidence = 8.0
    return state
