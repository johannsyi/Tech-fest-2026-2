import flet as ft
import sqlite3
from datetime import datetime

 

 

def connect_db():
    conn = sqlite3.connect("you.db")
    cursor = conn.cursor()

 

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        display_name TEXT UNIQUE,
        age_range TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        total_score INTEGER,
        category TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

