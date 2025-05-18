"""
This module contains a class for connecting to a PostgreSQL database.
"""

import psycopg2.pool
from .base import DatabaseConnector

class PostgresConnector(DatabaseConnector):
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str, minconn: int = 1, maxconn: int = 10):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

        # Create a connection pool instead of single connections
        self.pool = psycopg2.pool.SimpleConnectionPool(
            minconn=minconn,
            maxconn=maxconn,
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            sslmode="require"  # Use SSL for secure connections
        )

    def execute_query(self, query: str):
        """Get a connection from the pool, execute the query, and return the result."""
        conn = self.pool.getconn()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        finally:
            self.pool.putconn(conn)  # Return connection to the pool

    def get_schema(self):
        """Retrieve the schema of all tables in a PostgreSQL database."""
        schema = self.execute_query("SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema = 'public';")
        return {table: schema for table, schema in schema}
    
    def close(self):
        """Close all connections in the pool."""
        self.pool.closeall()
