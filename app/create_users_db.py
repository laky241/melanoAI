# app/create_users_db.py

import sqlite3
from passlib.hash import bcrypt
import os

# Ensure the DB is created in the app/ directory
DB_PATH = os.path.join("app", "users.db")
os.makedirs("app", exist_ok=True)

# Initialize DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)''')

# Add a new user manually (run once for each user)
def add_user(username, name, email, password):
    hashed_pw = bcrypt.hash(password)
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (username, name, email, hashed_pw))
        conn.commit()
        print(f"✅ User {username} added.")
    except sqlite3.IntegrityError:
        print(f"⚠️ Username '{username}' already exists.")

# ✏️ Change values here for a fresh start
add_user("demo", "Demo User", "demo@example.com", "demo123")

conn.close()
