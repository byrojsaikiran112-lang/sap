import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "ai_lms.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            course TEXT NOT NULL,
            topic TEXT NOT NULL,
            level TEXT NOT NULL,
            mode TEXT NOT NULL,
            output TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generation_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(generation_id) REFERENCES generations(id)
        )
    """)
    conn.commit()
    conn.close()

def save_generation(student_name, course, topic, level, mode, output):
    conn = get_connection()
    cur = conn.execute("""
        INSERT INTO generations
        (student_name, course, topic, level, mode, output)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (student_name, course, topic, level, mode, output))
    conn.commit()
    generation_id = cur.lastrowid
    conn.close()
    return generation_id

def get_history(limit=20):
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, student_name, course, topic, level, mode, output, created_at
        FROM generations
        ORDER BY id DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_feedback(generation_id, rating, comment):
    conn = get_connection()
    conn.execute("""
        INSERT INTO feedback (generation_id, rating, comment)
        VALUES (?, ?, ?)
    """, (generation_id, rating, comment))
    conn.commit()
    conn.close()
