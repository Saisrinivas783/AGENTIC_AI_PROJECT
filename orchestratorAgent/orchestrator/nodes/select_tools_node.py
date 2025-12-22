from schemas.state import OrchestratorState, ToolCall

def select_tools_node(state: OrchestratorState, registry: dict) -> OrchestratorState:
    tools = registry.get("tools", [])
    tool_names = [t.get("name") for t in tools if t.get("name")]

    state.selected_tool_candidates = tool_names

    chosen = "IBTAgent" if "IBTAgent" in tool_names else (tool_names[0] if tool_names else "")

    state.selected_tools = []
    if chosen:
        state.selected_tools.append(
            ToolCall(
                tool_name=chosen,
                reason=f"Selected based on intent='{state.intent}' (stub rule)",
                confidence=9.0,
                parameters={}
            )
        )

    state.messages.append(f"Select tools node: chosen={chosen}, candidates={tool_names}")
    return state
