"""
This module defines the abstract base class for database connectors.
"""

import abc

class DatabaseConnector(abc.ABC):
    """Abstract base class for database connectors."""
    
    @abc.abstractmethod
    def connect(self):
        """Establish a connection to the database."""
        pass
    
    @abc.abstractmethod
    def execute_query(self, query: str):
        """Execute a SQL query and return results."""
        pass

    @abc.abstractmethod
    def close(self):
        """Close the database connection."""
        pass
