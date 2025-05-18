"""
Simple test runner for the SQL Agent without FastAPI.
Connects to a SQLite database and runs a natural language query.
"""

from connectors.sqlite import SQLiteConnector
from agents.graph import build_sql_agent

def main():
    # Path to your Netflix .db file
    db_path = "netflixdb.sqlite"

    # Connect to the SQLite database
    db = SQLiteConnector(db_path)
    db.connect()

    # Get the database schema
    schema = db.get_schema()

    # Build the LangGraph agent
    agent = build_sql_agent()

    # Define the agent's initial state
    initial_state = {
        "query": [{"content": "What are the top 5 movies?", "type": "human"}],
        "sql_query": None,
        "schema": schema,
        "result": None,
        "db_type": "sqlite",
        "db_connector": db
    }

    # Invoke the agent
    final_state = agent.invoke(initial_state)

    # Print results
    print("\n--- Agent Run Result ---")
    print("Generated SQL Query:\n", final_state["sql_query"])
    print("\nExecution Result:\n", final_state["result"])

    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()
