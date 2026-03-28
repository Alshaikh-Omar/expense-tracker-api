import sqlite3
DB = sqlite3.connect('expenses.db')
def get_connection():
    return sqlite3.connect('expenses.db')

def create_table():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS expenses (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     expense TEXT NOT NULL,
     amount REAL NOT NULL,
     date TEXT NOT NULL
     )
     """)
    conn.commit()
    conn.close()