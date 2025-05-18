import os
import pytest
from connectors.sqlite import SQLiteConnector
from connectors.postgres import PostgresConnector

# Load environment variables (if using .env file)
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
    "dbname": os.getenv("POSTGRES_DB", "test_db"),
    "user": os.getenv("POSTGRES_USER", "test_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "test_password"),
}

def test_sqlite_connection():
    """Test SQLite database connection."""
    db = SQLiteConnector("test.db")
    db.connect()
    db.execute_query("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute_query("INSERT INTO test (name) VALUES ('Sample')")
    db.execute_query("INSERT INTO test (name) VALUES ('Another sample')")
    db.execute_query("INSERT INTO test (name) VALUES ('Yet another sample')")
    db.execute_query("INSERT INTO test (name) VALUES ('Last sample')")
    result = db.execute_query("SELECT * FROM test")
    assert len(result) > 0
    print(result)
    print(f"Database Schema: {db.get_schema()}")
    db.close()

def test_postgres_connection():
    """Test PostgreSQL database connection."""
    db = PostgresConnector(**POSTGRES_CONFIG)
    db.execute_query("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT)")
    db.execute_query("INSERT INTO test (name) VALUES ('Sample')")
    db.execute_query("INSERT INTO test (name) VALUES ('Another sample')")
    db.execute_query("INSERT INTO test (name) VALUES ('Yet another sample')")
    db.execute_query("INSERT INTO test (name) VALUES ('Last sample')")
    result = db.execute_query("SELECT * FROM test")
    assert len(result) > 0
    print(result)
    print(f"Database Schema: {db.get_schema()}")
    db.close()

if __name__ == "__main__":
    test_sqlite_connection()
    print("✅ SQLite connection test passed.")
    
    # test_postgres_connection()
    # print("✅ PostgreSQL connection test passed.")
