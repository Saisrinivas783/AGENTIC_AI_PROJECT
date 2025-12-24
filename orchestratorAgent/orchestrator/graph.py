from langgraph.graph import StateGraph, START, END
from schemas.state import OrchestratorState

from orchestrator.nodes.intent_node import intent_node
from orchestrator.nodes.select_tools_node import select_tools_node
from orchestrator.nodes.tool_exec import tool_exec_node
from orchestrator.nodes.response_compose import response_compose_node

def build_graph():
    workflow = StateGraph(OrchestratorState)

    workflow.add_node("intent", intent_node)
    workflow.add_node("select_tools", select_tools_node)
    workflow.add_node("call_tools", tool_exec_node)
    workflow.add_node("response", response_compose_node)

    workflow.set_entry_point("intent")
    workflow.add_edge("intent", "select_tools")
    workflow.add_edge("select_tools", "call_tools")
    workflow.add_edge("call_tools", "response")
    workflow.add_edge("response", END)

    return workflow.compile()
