import sqlite3
import datetime
import getpass

# Verilənlər bazasını yaradırıq
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Cədvəlləri yaradırıq
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    passkey TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    timestamp TEXT
)
""")
conn.commit()