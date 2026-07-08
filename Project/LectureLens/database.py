import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("lecturelens.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            summary TEXT NOT NULL,
            quiz TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_result(url, summary, quiz):
    conn = sqlite3.connect("lecturelens.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (url, summary, quiz, created_at) VALUES (?, ?, ?, ?)",
        (url, summary, quiz, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect("lecturelens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, summary, quiz, created_at FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database created successfully!")
