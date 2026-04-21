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
