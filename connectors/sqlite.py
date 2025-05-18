"""
SQLite database connector.
"""

import sqlite3
from .base import DatabaseConnector

class SQLiteConnector(DatabaseConnector):
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn = None

    def connect(self):
        """Connect to the SQLite database."""
        self.conn = sqlite3.connect(self.db_file)

    def get_schema(self):
        """Retrieve the schema of all tables in an SQLite database."""
        schema = self.execute_query("SELECT name, sql FROM sqlite_master WHERE type='table';")        
        return {table: sql for table, sql in schema}

    def execute_query(self, query: str):
        """Execute a SQL query and return results."""
        if not self.conn:
            raise ConnectionError("Database not connected.")
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
