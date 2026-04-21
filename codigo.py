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

 

            try:
                answers = [
                    int(q1.value), int(q2.value),
                    int(q3.value), int(q4.value),
                    int(q5.value)
                ]
            except:
                page.snack_bar = ft.SnackBar(ft.Text("Answer all questions"))
                page.snack_bar.open = True
                page.update()
                return

 

            score, category = calculate_score(answers)

 

            conn = sqlite3.connect("you.db")
            cursor = conn.cursor()

 

            try:
                cursor.execute("INSERT INTO users (display_name, age_range) VALUES (?, ?)",
                               (name.value, age.value))
                user_id = cursor.lastrowid

 

                cursor.execute(
                    "INSERT INTO results (user_id, total_score, category, created_at) VALUES (?, ?, ?, ?)",
                    (user_id, score, category, datetime.now())
                )

 

                conn.commit()
            except:
                page.snack_bar = ft.SnackBar(ft.Text("Name already exists"))
                page.snack_bar.open = True
                page.update()
                return

 

            conn.close()

 

            show_result(name.value, score, category)

 

        return ft.Column([
            ft.Text("Create Profile", size=25),
            name,
            age,
            q1, q2, q3, q4, q5,
            ft.ElevatedButton("Submit", on_click=submit),
            ft.ElevatedButton("Back", on_click=go_home)
        ], scroll="auto")

def show_result(name, score, category):
        conn = sqlite3.connect("you.db")
        cursor = conn.cursor()

 

        cursor.execute("""
        SELECT display_name, total_score FROM users
        JOIN results ON users.id = results.user_id
        ORDER BY total_score DESC
        """)

 

        all_users = cursor.fetchall()

 

        rank = [u[0] for u in all_users].index(name) + 1
        total = len(all_users)

 

        conn.close()

 

        page.controls.clear()
        page.add(ft.Column([
            ft.Text(f"{name}'s Result", size=25),
            ft.Text(f"Score: {score}"),
            ft.Text(f"Category: {category}"),
            ft.Text(f"Rank: #{rank} out of {total}"),
            ft.ElevatedButton("Leaderboard", on_click=go_leaderboard),
            ft.ElevatedButton("Home", on_click=go_home)
        ]))

 

    
    def leaderboard_view():
        conn = sqlite3.connect("you.db")
        cursor = conn.cursor()

 

        cursor.execute("""
        SELECT display_name, total_score, category
        FROM users
        JOIN results ON users.id = results.user_id
        ORDER BY total_score DESC
        """)

 

        rows = cursor.fetchall()
        conn.close()

 

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Rank")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Score")),
                ft.DataColumn(ft.Text("Category")),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(i+1))),
                    ft.DataCell(ft.Text(r[0])),
                    ft.DataCell(ft.Text(str(r[1]))),
                    ft.DataCell(ft.Text(r[2]))
                ]) for i, r in enumerate(rows)
            ]
        )

return ft.Column([
            ft.Text("Leaderboard", size=25),
            table,
            ft.ElevatedButton("Back", on_click=go_home)
        ], scroll="auto")

 

    go_home()
