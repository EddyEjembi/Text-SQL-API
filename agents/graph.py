"""
This module defines the SQL agent graph using the LangGraph library.   
"""
from langgraph.graph import StateGraph, END
from agents.nodes import generate_sql_node, execute_query_node, AgentState

def build_sql_agent():
    graph = StateGraph(AgentState)

    graph.add_node("generate_sql", generate_sql_node)
    graph.add_node("execute_sql", execute_query_node)

    graph.set_entry_point("generate_sql")
    graph.add_edge("generate_sql", "execute_sql")
    graph.add_edge("execute_sql", END)

    compiled = graph.compile()

    # Log every state
    """def log_state(state):
        print("Current State:", state)
        return state

    compiled.add_hook(log_state)"""

    return compiled