"""
database.py
------------
Handles the SQLite connection and table creation.

We use Python's built-in `sqlite3` module directly (no ORM like SQLAlchemy)
to keep the exercise simple and to make it very clear exactly what SQL is
being run.
"""

import sqlite3

DB_NAME = "tickets.db"


def get_db_connection():
    """
    Opens a new connection to the SQLite database file.

    conn.row_factory = sqlite3.Row lets us access columns by name
    (row["title"]) instead of only by index (row[1]), which makes the
    code in main.py much more readable.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates the `tickets` table if it doesn't already exist.
    Called once when the app starts up.

    Note: `tags` is a plain TEXT column holding a comma-separated string
    (e.g. "billing,urgent") as required by the assignment — there is no
    separate tags table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            tags TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
