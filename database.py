import sqlite3
DB = sqlite3.connect('expenses.db')
def get_connection():
    return sqlite3.connect('expenses.db')

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
     CREATE TABLE IF NOT EXISTS users (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     username TEXT UNIQUE,
     password TEXT
     )
     """)

    conn.commit()
    conn.close()