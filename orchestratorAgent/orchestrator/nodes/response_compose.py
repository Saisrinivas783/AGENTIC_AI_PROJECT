from schemas.state import OrchestratorState

def response_compose_node(state: OrchestratorState) -> OrchestratorState:
    if state.selected_tools:
        state.selected_tool_name = state.selected_tools[0].tool_name
        state.selected_tool_confidence = state.selected_tools[0].confidence
    else:
        state.selected_tool_name = "Unknown"
        state.selected_tool_confidence = 0.0

    state.final_answer = "" 
    state.messages.append("STUB response_compose: completed")
    return state
