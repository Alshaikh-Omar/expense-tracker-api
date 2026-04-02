from database import get_connection
from datetime import date
from passlib.hash import bcrypt
import csv
import sqlite3
def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print("Unexpected error:", e)
        return False

    finally:
        conn.close()

def verify_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if user and bcrypt.verify(password, user[0]):
        return True

    return False

def add_expense(expense, amount, category):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (expense, amount, category, date) VALUES (?,?,?,?)",
        (expense, amount, category, date.today().isoformat())
    )

    conn.commit()
    conn.close()
    print("Successfully added expense\n")

def get_all_expenses(limit: int = 5, offset: int = 0, sort_by= "id", category= None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT rowid, expense, amount, category, date FROM expenses"
    params = []

    # filter by category
    if category:
        query += " WHERE category = ?"
        params.append(category)

    # sorting
    if sort_by =="amount":
        query += " ORDER BY amount ASC"
    elif sort_by == "date":
        query += " ORDER BY date ASC"
    else:
        query += " ORDER BY rowid ASC"

    # pagination
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = cursor.execute(query, tuple(params)).fetchall()

    conn.close()

    return[
        {
            "id": row[0],
            "expense": row[1],
            "amount": row[2],
            "category": row[3],
            "date": row[4]
        }
        for row in rows
    ]


def delete_expense(expense_id):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM expenses WHERE rowid = ?", (expense_id,)
    )
    conn.commit()

    deleted = cursor.rowcount
    conn.close()
    return deleted > 0

def total_spent():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    result = cursor.fetchone()
    conn.close()

    total = result[0]
    if total is None:
        print("No expenses\n")
    else:
        print(f"Total expenses: {total:.2f}\n")

def monthly_spent():
    today = date.today()
    month_key = today.strftime("%Y-%m")
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute("""SELECT SUM(amount)
    FROM expenses
    WHERE substr(date, 1, 7) = ?
    """, (month_key, )).fetchone()
    conn.close()
    total = result[0]
    if total is None:
        print("No expenses this month\n")
    else:
        print(f"this month's total: {total:.2f}\n")


def search_expenses(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        "SELECT rowid, expense, amount, category, date FROM expenses WHERE expense LIKE ? OR category LIKE ?",
        (f"%{keyword}%", f"%{keyword}%")
    ).fetchall()

    conn.close()

    return [
        {
            "ID": row[0],
            "expense": row[1],
            "amount": row[2],
            "category": row[3],
            "date": row[4]
        }
        for row in rows
    ]

def get_expense(expense_id):

    conn = get_connection()
    cursor = conn.cursor()

    row = cursor.execute("""SELECT expense, amount, category FROM expenses WHERE rowid = ?""", (expense_id,)).fetchone()

    conn.close()

    return row

def edit_expense(expense_id, new_name, new_amount, new_category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" UPDATE expenses SET expense = ?, amount = ?, category = ? WHERE rowid = ? """, (new_name, new_amount, new_category, expense_id))

    conn.commit()

    edited = cursor.rowcount
    conn.close()
    return edited > 0

def export_csv():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT rowid, expense, amount, category, date FROM expenses").fetchall()
    conn.close()

    with open("expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID","Expense","Amount","category","Date"])
        writer.writerows(rows)

    print("Expense exported to csv\n")

def category_stats():
    conn = get_connection()
    cursor = conn.cursor()
    rows = cursor.execute("""SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC """).fetchall()
    conn.close()
    if not rows:
        print("No expenses found\n")
        return
    print(f"\nCategory | Total spent")
    print("-"*25)
    for row in rows:
        print(f"{row[0]:<8} | {row[1]:.2f}")
    print()

def get_expense_by_id(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT rowid, expense, amount, category, date FROM expenses WHERE rowid = ?", (expense_id,)).fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "expense": row[1],
        "amount": row[2],
        "category": row[3],
        "date": row[4]

    }