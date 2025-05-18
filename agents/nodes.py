"""
LangGraph nodes that handle SQL generation and execution.
"""
from typing import List, TypedDict, Annotated, Optional, Union
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from connectors.postgres import PostgresConnector
from connectors.sqlite import SQLiteConnector
from agents.tools import generate_sql, execute_query, tools

# Define the agent state as a TypedDict for better type checking
class AgentState(TypedDict):
    """
    State of the agent, including query and schema.
    """
    query: Annotated[list[AnyMessage], add_messages]
    sql_query: str
    schema: List[dict]
    result: Optional[Union[List[dict], str]]
    db_type: str
    db_connector: Union[PostgresConnector, SQLiteConnector, None]


def generate_sql_node(state: AgentState) -> AgentState:
    sql_query = generate_sql(
        query=state["query"][-1].content,
        db_type=state["db_type"],
        schema=state["schema"]
    )
    print(f"Generated SQL Query: {sql_query}")
    return {**state, "sql_query": sql_query}

def execute_query_node(state: AgentState) -> AgentState:
    result = execute_query(state["db_connector"], state["sql_query"])
    print(f"Execution Result: {result}")
    return {**state, "result": result}