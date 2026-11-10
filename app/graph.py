from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from app.state import AgentState
from app.nodes import router_node, food_node, sport_node, response_node


def build_graph():
    """Собирает и компилирует LangGraph-агента с памятью."""
    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("food", food_node)
    builder.add_node("sport", sport_node)
    builder.add_node("response", response_node)

    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",
        lambda state: state["intent"],
        {"food": "food", "sport": "sport", "general": "response"},
    )
    builder.add_edge("food", "response")
    builder.add_edge("sport", "response")
    builder.add_edge("response", END)

    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)


graph = build_graph()