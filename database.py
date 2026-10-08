import sqlite3
import hashlib
from datetime import datetime

DB_NAME = "path_to_peace.db"

def connect():
    return sqlite3.connect(DB_NAME)

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS counselling_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            display_name TEXT NOT NULL,
            concern TEXT NOT NULL,
            preferred_date TEXT,
            preferred_time TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            admin_note TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS mood_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            mood TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

def create_default_admin():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if cur.fetchone() is None:
        cur.execute("""
            INSERT INTO users (full_name, username, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            "Path to Peace Counsellor",
            "admin",
            hash_password("admin123"),
            "admin"
        ))

    conn.commit()
    conn.close()

def register_user(full_name, username, password):
    conn = connect()
    try:
        conn.execute("""
            INSERT INTO users (full_name, username, password, role)
            VALUES (?, ?, ?, 'user')
        """, (full_name, username, hash_password(password)))
        conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "That username already exists."
    finally:
        conn.close()

def login_user(username, password):
    conn = connect()
    row = conn.execute("""
        SELECT id, full_name, username, role
        FROM users
        WHERE username = ? AND password = ?
    """, (username, hash_password(password))).fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "full_name": row[1],
            "username": row[2],
            "role": row[3]
        }
    return None

def add_counselling_request(user_id, display_name, concern, date, time):
    conn = connect()
    conn.execute("""
        INSERT INTO counselling_requests
        (user_id, display_name, concern, preferred_date, preferred_time, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'Pending', ?)
    """, (
        user_id, display_name, concern, date, time,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    conn.close()

def get_user_requests(user_id):
    conn = connect()
    rows = conn.execute("""
        SELECT id, display_name, concern, preferred_date, preferred_time,
               status, admin_note, created_at
        FROM counselling_requests
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()
    conn.close()
    return rows

def get_all_requests():
    conn = connect()
    rows = conn.execute("""
        SELECT id, display_name, concern, preferred_date, preferred_time,
               status, admin_note, created_at
        FROM counselling_requests
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return rows

def update_request(request_id, status, admin_note=""):
    conn = connect()
    conn.execute("""
        UPDATE counselling_requests
        SET status = ?, admin_note = ?
        WHERE id = ?
    """, (status, admin_note, request_id))
    conn.commit()
    conn.close()

def add_mood_entry(user_id, mood, note):
    conn = connect()
    conn.execute("""
        INSERT INTO mood_entries (user_id, mood, note, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, mood, note, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def get_mood_entries(user_id, limit=10):
    conn = connect()
    rows = conn.execute("""
        SELECT mood, note, created_at
        FROM mood_entries
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return rows

def request_counts():
    conn = connect()
    total = conn.execute("SELECT COUNT(*) FROM counselling_requests").fetchone()[0]
    pending = conn.execute(
        "SELECT COUNT(*) FROM counselling_requests WHERE status='Pending'"
    ).fetchone()[0]
    accepted = conn.execute(
        "SELECT COUNT(*) FROM counselling_requests WHERE status='Accepted'"
    ).fetchone()[0]
    cancelled = conn.execute(
        "SELECT COUNT(*) FROM counselling_requests WHERE status='Cancelled'"
    ).fetchone()[0]
    conn.close()
    return total, pending, accepted, cancelled
