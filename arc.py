import hashlib
import sqlite3
import functools

STATUS_DB = "arc_status.db"


def init_db():
    conn = sqlite3.connect(STATUS_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS call_status (
        call_hash TEXT PRIMARY KEY,
        status TEXT
    )""")
    conn.commit()
    conn.close()


def _hash_call(func_name, args, kwargs):
    key = f"{func_name}:{args}:{kwargs}"
    return hashlib.sha256(key.encode()).hexdigest()


def idempotent(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        init_db()
        call_hash = _hash_call(func.__name__, args, kwargs)
        conn = sqlite3.connect(STATUS_DB)
        row = conn.execute("SELECT status FROM call_status WHERE call_hash = ?", (call_hash,)).fetchone()

        if row and row[0] in ("processing", "done"):
            conn.close()
            return {"status": "skipped", "reason": row[0]}

        conn.execute(
            "INSERT INTO call_status (call_hash, status) VALUES (?, 'processing') "
            "ON CONFLICT(call_hash) DO UPDATE SET status = 'processing'",
            (call_hash,)
        )
        conn.commit()
        conn.close()

        try:
            result = func(*args, **kwargs)
            conn = sqlite3.connect(STATUS_DB)
            conn.execute("UPDATE call_status SET status = 'done' WHERE call_hash = ?", (call_hash,))
            conn.commit()
            conn.close()
            return result
        except Exception:
            conn = sqlite3.connect(STATUS_DB)
            conn.execute("UPDATE call_status SET status = 'failed' WHERE call_hash = ?", (call_hash,))
            conn.commit()
            conn.close()
            raise
    return wrapper