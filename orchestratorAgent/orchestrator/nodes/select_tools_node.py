from schemas.state import OrchestratorState
from schemas.tools import SelectedTools


def select_tools_node(state: OrchestratorState) -> OrchestratorState:
    registry = state.registry or {}
    tools = registry.get("tools", [])
    tool_names = [t.get("name") for t in tools if t.get("name")]

    chosen = "IBTAgent" if "IBTAgent" in tool_names else (tool_names[0] if tool_names else "")

    state.selected_tools = []
    if chosen:
        state.selected_tools.append(
            SelectedTools(
                tool_name=chosen,
                reason=f"Selected based on intent='{state.intent}' (stub rule)",
                confidence=9.0,
                parameters={},
            )
        )

    return state
