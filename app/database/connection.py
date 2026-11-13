import sqlite3
from pathlib import Path

DB_PATH = "data/audit.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_token TEXT NOT NULL UNIQUE,
    consent_given INTEGER NOT NULL DEFAULT 0,
    started_at DATETIME NOT NULL,
    finished_at DATETIME
);
CREATE TABLE IF NOT EXISTS keyboard_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES sessions(id),
    event_type TEXT NOT NULL,
    key_category TEXT NOT NULL,
    context TEXT NOT NULL,
    timestamp DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('auditor', 'admin')),
    created_at DATETIME NOT NULL
);
CREATE TABLE IF NOT EXISTS access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT NOT NULL,
    detail TEXT,
    timestamp DATETIME NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_time ON keyboard_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_session ON keyboard_events(session_id);
"""


def get_connection(db_path=DB_PATH):
    if str(db_path) != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
