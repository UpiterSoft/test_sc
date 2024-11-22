import sqlite3
import json
from datetime import datetime

DB_PATH = "search_history.db"

def initialize_db():
    """
    Initialize the database and create tables if not exists.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                max_results INTEGER NOT NULL,
                results TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_query(query, max_results, results):
    """
    Save a query and its results into the database.

    Args:
        query (str): The search query.
        max_results (int): Number of results.
        results (list): List of tuples (link, score).
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO queries (query, max_results, results)
            VALUES (?, ?, ?)
        """, (query, max_results, json.dumps(results)))
        conn.commit()

def get_cached_results(query, max_results):
    """
    Retrieve cached results for a given query if available.

    Args:
        query (str): The search query.
        max_results (int): Number of results.

    Returns:
        list or None: Cached results or None if not found.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT results FROM queries
            WHERE query = ? AND max_results = ?
            ORDER BY timestamp DESC LIMIT 1
        """, (query, max_results))
        row = cursor.fetchone()
        return json.loads(row[0]) if row else None

def get_recent_queries(limit=100):
    """
    Retrieve the most recent queries.

    Args:
        limit (int): Maximum number of queries to fetch.

    Returns:
        list: List of recent queries with their details.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT query, max_results, timestamp
            FROM queries
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()
