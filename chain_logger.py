import sqlite3
import uuid
from datetime import datetime

CHAIN_DB = "chain_log.db"


def init_chain_db():
    conn = sqlite3.connect(CHAIN_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS chain_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT,
        step_number INTEGER,
        tool_called TEXT,
        timestamp TEXT
    )""")
    conn.commit()
    conn.close()


def new_run_id():
    return str(uuid.uuid4())


def log_step(run_id, step_number, tool_called):
    init_chain_db()
    conn = sqlite3.connect(CHAIN_DB)
    conn.execute(
        "INSERT INTO chain_log (run_id, step_number, tool_called, timestamp) VALUES (?, ?, ?, ?)",
        (run_id, step_number, tool_called, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_chain(run_id):
    conn = sqlite3.connect(CHAIN_DB)
    rows = conn.execute(
        "SELECT step_number, tool_called, timestamp FROM chain_log WHERE run_id = ? ORDER BY step_number",
        (run_id,)
    ).fetchall()
    conn.close()
    return rows