
from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("team.db")

def create_table():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            available INTEGER DEFAULT 0
        )
    """)

    count = db.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if count == 0:
        db.executemany(
            "INSERT INTO users (name, available) VALUES (?, ?)",
            [
                ("Harshini", 0),
                ("Arun", 1),
                ("Priya", 0),
                ("Kumar", 1)
            ]
        )

    db.commit()
    db.close()


@app.route("/")
def home():
    db = get_db()

    users = db.execute(
        "SELECT * FROM users"
    ).fetchall()

    db.close()

    return render_template("index.html", users=users)


@app.route("/toggle/<int:user_id>", methods=["POST"])
def toggle(user_id):
    db = get_db()

    db.execute("""
        UPDATE users
        SET available = 1 - available
        WHERE id = ?
    """, (user_id,))

    db.commit()
    db.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
