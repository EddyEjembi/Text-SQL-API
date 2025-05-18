"""
This module contains the FastAPI routes for the database connector API.
"""
from fastapi import APIRouter, HTTPException
from api import models

from connectors.sqlite import SQLiteConnector
from connectors.postgres import PostgresConnector
from langchain_community.utilities import SQLDatabase
#from agents.graph import build_sql_agent
from agents.sql_agent import sql_agent

router = APIRouter()
db_connection = None
db_type = None


def get_db_connector(**kwargs):
    if kwargs.get("db_type") == "sqlite":
        print(kwargs.get("db_path"))
        #db = SQLiteConnector(kwargs.get("db_path"))
        #db.connect()
        db = SQLDatabase.from_uri(f"sqlite:///{kwargs.get('db_path')}")
        #schema = db.get_schema()
        print(f"Database Schema: {db.get_usable_table_names()}")
        return db #, schema
    elif kwargs.get("db_type") == "postgres":
        db = PostgresConnector(**kwargs)
        #schema = db.get_schema()
        print(f"Database Schema: {db.get_schema()}")
        return db #, schema
    else:
        raise ValueError("Unsupported database type. Currently supported: sqlite, postgres")

@router.get("/")
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Database Connector API is running",
            "available_databases": ["sqlite", "postgres"],
            "To Connect": "POST /connect",
            "To Disconnect": "POST /disconnect",
            "To Execute SQL": "POST /sql-query",
            "To Execute SQL with Agent": "POST /query",
            "Query Payload": {
                "question": "What is the question?",
                "model": "Select a model (e.g., 'gemini-2.0-flash')",
                "provider": "Select a provider (e.g., 'google_genai')",
                "api_key": "your_api_key"
            },
            "Query Note": "Install the required LangChain package for your model provider. E.g., 'google_genai' requires 'langchain-google', openai requires 'langchain-openai', etc.",
        }

@router.post("/connect")
async def connect_db(payload: models.DBConnector):
    """
    Connect to the database and return the schema. db_type can be either 'sqlite' or 'postgres'.
    The payload should contain the necessary connection parameters.
    For SQLite, provide db_path. For Postgres, provide 'host', 'port', 'dbname', 'user', and 'password'.
    """
    global db_connection
    global db_type
    try:
        db_type = payload.db_type
        #
        # print(f"Database Type: {db_type, type(db_type)}")
        db_connection = get_db_connector(**payload.dict())
        print(f"DB Connection Type: {db_type}")

        if db_type == "sqlite":
            return {"message": f"Connected to {db_type} Database successfully",
                    "Schema": db_connection.table_info
                    }
        elif db_type == "postgres":
            return {"message": f"Connected to {db_type} Database successfully",
                    "Schema": db_connection.get_schema()
                    }
        else:
            raise HTTPException(status_code=400, detail="Unsupported database type. Currently supported: sqlite, postgres")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sql-query")
async def execute_query(payload: models.QueryPayload):
    """
    Execute a SQL query directly on the database.
    Payload should contain the SQL query string.
    """
    global db_connection
    print(f"DB Connection: {db_connection}")
    if not db_connection:
        raise HTTPException(status_code=400, detail="No database connection")
    try:
        print(payload.query, type(payload.query))
        result = db_connection.execute_query(payload.query)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

"""@router.post("/query")
async def execute_query(payload: models.QueryPayload):
    global db_connection
    global db_type
    if not db_connection:
        raise HTTPException(status_code=400, detail="Database not connected.")

    try:
        schema = db_connection.get_schema()
        agent = build_sql_agent()

        initial_state = {
            "query": [payload.query],
            "sql_query": None,
            "schema": schema,
            "result": None,
            "db_type": db_type,
            "db_connector": db_connection
        }

        final_state = agent.invoke(initial_state)
        return {"sql_query": final_state["sql_query"], "result": final_state["result"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))"""

@router.post("/query")
async def execute_query(payload: models.SQLAgentPayload):
    """
    Execute a SQL query using the SQL agent.
    Payload should contain the question, model, provider, and api_key.
    """
    global db_connection
    global db_type
    if not db_connection:
        raise HTTPException(status_code=400, detail="Database not connected.")

    try:
        agent = sql_agent(db_connection, payload.question, payload.model, payload.provider, payload.api_key)

        return {"response": agent}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/disconnect")
async def disconnect_db():
    """
    Disconnect from the database.
    """
    global db_connection
    if db_connection:
        db_connection.close()
        db_connection = None
    return {"message": "Database disconnected"}