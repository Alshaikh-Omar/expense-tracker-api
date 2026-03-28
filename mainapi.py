from fastapi import FastAPI, HTTPException
from models import Expense, ExpenseOut
from operations import (get_all_expenses, add_expense, delete_expense, edit_expense, search_expenses, get_expense_by_id)

app = FastAPI()



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
def create_expense(exp: Expense):
    add_expense(exp.expense, exp.amount, exp.category)
    return {"message": "Expense added"}


@app.delete("/expenses/{expense_id}", status_code=200)
def delete_expense_api(expense_id: int):
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


