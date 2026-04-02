from fastapi import FastAPI, HTTPException
from models import Expense, ExpenseOut, User
from operations import (get_all_expenses, add_expense, delete_expense, edit_expense, search_expenses, get_expense_by_id, create_user, verify_user)

app = FastAPI()

def fake_auth(username: str, password: str):
    valid = verify_user(username, password)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/register")
def register(user: User):
    success = create_user(user.username, user.password)

    if not success:
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "User created"}

@app.post("/login")
def login(user: User):
    valid = verify_user(user.username, user.password)

    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}


@app.get("/expenses", response_model=list[ExpenseOut])
def get_expenses(
        limit: int = 5,
        offset: int = 0,
        sort_by: str = "id",
        category: str | None = None
):
    success = get_all_expenses(limit, offset, sort_by, category)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")

    return success


@app.get("/expenses/search")
def search_expenses_api(keyword: str):
    return search_expenses(keyword)


@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense_api(expense_id: int):
    expense = get_expense_by_id(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.post("/expenses", status_code=201)
def create_expense(exp: Expense, username: str, password: str):
    fake_auth(username, password)
    add_expense(exp.expense, exp.amount, exp.category)
    return {"message": "Expense added"}


@app.delete("/expenses/{expense_id}", status_code=200)
def delete_expense_api(expense_id: int, username: str, password: str):
    fake_auth(username, password,)
    success = delete_expense(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense deleted"}


@app.put("/expenses/{expense_id}")
def update_expense_api(expense_id: int, exp: Expense):
    success = edit_expense(expense_id, exp.expense, exp.amount, exp.category)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense updated"}


