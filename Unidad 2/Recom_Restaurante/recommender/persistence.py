import sqlite3
from pathlib import Path
from typing import Optional, Dict

DB_PATH = Path("feedback.db")

DDL = '''
CREATE TABLE IF NOT EXISTS feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  user_id TEXT,
  dish_id TEXT NOT NULL,
  like INTEGER NOT NULL CHECK (like IN (0,1))
);
CREATE INDEX IF NOT EXISTS idx_feedback_dish ON feedback(dish_id);
CREATE INDEX IF NOT EXISTS idx_feedback_user ON feedback(user_id);
'''

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_conn()
    with conn:
        conn.executescript(DDL)
    conn.close()

def add_feedback(dish_id: str, like: bool, user_id: Optional[str] = None):
    conn = get_conn()
    with conn:
        conn.execute("INSERT INTO feedback(ts, user_id, dish_id, like) VALUES(datetime('now'), ?, ?, ?)", 
                     (user_id, dish_id, 1 if like else 0))
    conn.close()

def dish_like_ratio(dish_id: str) -> Optional[float]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), SUM(like) FROM feedback WHERE dish_id=?", (dish_id,))
    n, s = cur.fetchone()
    conn.close()
    if n == 0:
        return None
    return (s or 0) / n

def global_like_ratios() -> Dict[str, float]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT dish_id, COUNT(*), SUM(like) FROM feedback GROUP BY dish_id")
    out = {}
    for dish_id, n, s in cur.fetchall():
        if n and n > 0:
            out[dish_id] = (s or 0)/n
    conn.close()
    return out
