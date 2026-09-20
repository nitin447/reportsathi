import sqlite3
from datetime import datetime, timezone

import bcrypt

DB_PATH = "reportsathi.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def signup(name: str, email: str, password: str) -> tuple[bool, str]:
    email = email.strip().lower()
    if not name.strip() or not email or len(password) < 6:
        return False, "Please fill in your name, email, and a password of at least 6 characters."
    conn = get_conn()
    try:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        conn.execute(
            "INSERT INTO users (email, name, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (email, name.strip(), hashed, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return True, "Account created. Please log in."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    finally:
        conn.close()


def login(email: str, password: str) -> tuple[bool, str, dict | None]:
    email = email.strip().lower()
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    if not row:
        return False, "No account found with this email.", None
    user_id, name, password_hash = row
    if not bcrypt.checkpw(password.encode(), password_hash.encode()):
        return False, "Incorrect password.", None
    return True, "Logged in.", {"id": user_id, "name": name, "email": email}

def find_or_create_google_user(name: str, email: str) -> dict:
    """Google sign-in: reuse the account if the email exists, else create one with no password."""
    email = email.strip().lower()
    conn = get_conn()
    row = conn.execute("SELECT id, name FROM users WHERE email = ?", (email,)).fetchone()
    if row:
        user_id, existing_name = row
        conn.close()
        return {"id": user_id, "name": existing_name, "email": email}

    random_password_hash = bcrypt.hashpw(bcrypt.gensalt(), bcrypt.gensalt()).decode()
    conn.execute(
        "INSERT INTO users (email, name, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (email, name, random_password_hash, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    user_id = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()[0]
    conn.close()
    return {"id": user_id, "name": name, "email": email}