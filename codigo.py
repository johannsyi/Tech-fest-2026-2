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

conn.commit()
    conn.close()

 

#Score
def calculate_score(answers):
    score = sum(answers)

 

    if score <= 30:
        category = "Standard"
    elif score <= 60:
        category = "Rising"
    elif score <= 85:
        category = "Trending"
    else:
        category = "Premium"

 

    return score, category

 

 

def main(page: ft.Page):
    page.title = "YOU™ Simulator"
    page.theme_mode = "light"

 

    connect_db()

 

    
    def go_home(e=None):
        page.controls.clear()
        page.add(home_view())

 

    def go_form(e=None):
        page.controls.clear()
        page.add(form_view())

 

    def go_leaderboard(e=None):
        page.controls.clear()
        page.add(leaderboard_view())


