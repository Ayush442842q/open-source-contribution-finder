"""
Database initialization and connection management.
"""

import os
import sqlite3
import logging

logger = logging.getLogger(__name__)

DATABASE_PATH = os.getenv("DATABASE_PATH", "app.db")


def get_connection():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_database():
    """Initialize the database by running the schema."""
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    try:
        conn = get_connection()
        with open(schema_path, "r") as f:
            conn.executescript(f.read())
        conn.close()
        logger.info("[Database] Initialized successfully.")
    except Exception as e:
        logger.error(f"[Database] Initialization failed: {e}")
        raise
