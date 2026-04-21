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


# HOME
    def home_view():
        return ft.Column([
            ft.Text("YOU Social Value Simulator", size=30, weight="bold"),
            ft.Text("Discover your social value and ranking."),
            ft.ElevatedButton("Start Profile", on_click=go_form),
            ft.ElevatedButton("View Leaderboard", on_click=go_leaderboard)
        ], alignment="center")

 # QUESTIONS 
    def form_view():
        name = ft.TextField(label="Name")
        age = ft.Dropdown(
            label="Age Range",
            options=[
                ft.dropdown.Option("18-25"),
                ft.dropdown.Option("26-35"),
                ft.dropdown.Option("36+"),
            ]
        )

 

        # Questions (5)
        q1 = ft.RadioGroup(content=ft.Column([
            ft.Text("Are you extroverted?"),
            ft.Radio(value="10", label="Yes"),
            ft.Radio(value="5", label="No")
        ]))

 

        q2 = ft.RadioGroup(content=ft.Column([
            ft.Text("Do you take risks?"),
            ft.Radio(value="10", label="Often"),
            ft.Radio(value="5", label="Rarely")
        ]))

 

        q3 = ft.RadioGroup(content=ft.Column([
            ft.Text("Social media activity?"),
            ft.Radio(value="10", label="High"),
            ft.Radio(value="5", label="Low")
        ]))

 

        q4 = ft.RadioGroup(content=ft.Column([
            ft.Text("Leadership style?"),
            ft.Radio(value="10", label="Leader"),
            ft.Radio(value="5", label="Follower")
        ]))

 

        q5 = ft.RadioGroup(content=ft.Column([
            ft.Text("Decision making?"),
            ft.Radio(value="10", label="Fast"),
            ft.Radio(value="5", label="Slow")
        ]))

 

        def submit(e):
            if not name.value or not age.value:
                page.snack_bar = ft.SnackBar(ft.Text("Fill all fields"))
                page.snack_bar.open = True
                page.update()
                return
