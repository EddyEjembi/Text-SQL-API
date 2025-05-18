"""
This module contains the pydantic models for the API.
"""

from pydantic import BaseModel

class DBConnector(BaseModel):
    db_type: str
    db_path: str = None
    host: str = None
    port: int = None
    dbname: str = None
    user: str = None
    password: str = None

class QueryPayload(BaseModel):
    query: str

class SQLAgentPayload(BaseModel):
    question: str
    model: str
    provider: str
    api_key: str