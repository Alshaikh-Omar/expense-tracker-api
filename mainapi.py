from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException, Depends
from models import Expense, ExpenseOut, User, ExpenseListResponse
from operations import (get_all_expenses, add_expense, delete_expense, edit_expense, search_expenses, get_expense_by_id, create_user, verify_user)
from database import create_user_table, create_table
from auth import create_access_token, get_current_user

create_user_table()
create_table()

app = FastAPI(
    servers=[
        {"url": "https://expense-tracker-api-production-800b.up.railway.app", "description": "Production server"}
    ]
)

def fake_auth(username: str, password: str):
    valid = verify_user(username, password)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("pip/register")
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

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/expenses", response_model=ExpenseListResponse)
def get_expenses(user=Depends(get_current_user),
        limit: int = 5,
        offset: int = 0,
        sort_by: str = "id",
        category: str | None = None
):
    expenses = get_all_expenses(user, limit, offset, sort_by, category)


    return {
        "data": expenses,
        "count": len(expenses)
    }


@app.get("/expenses/search")
def search_expenses_api(keyword: str, user=Depends(get_current_user)):
    search = search_expenses(keyword, user)
    if search is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return search


@app.get("/expenses/{expense_id}", response_model=ExpenseOut)
def get_expense_api(expense_id: int, user=Depends(get_current_user)):
    expense = get_expense_by_id(expense_id, user)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


@app.post("/expenses", status_code=201)
def create_expense(exp: Expense, user=Depends(get_current_user)):
    add_expense(exp.expense, exp.amount, exp.category, user)
    return {"message": f"Added by {user}"}


@app.delete("/expenses/{expense_id}", status_code=200)
def delete_expense_api(expense_id: int, user=Depends(get_current_user)):
    success = delete_expense(expense_id, user)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": f"Expense deleted by {user}"}


@app.put("/expenses/{expense_id}")
def update_expense_api(expense_id: int, exp: Expense, user=Depends(get_current_user)):
    success = edit_expense(expense_id, exp.expense, exp.amount, exp.category, user)
    if not success:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense updated"}


