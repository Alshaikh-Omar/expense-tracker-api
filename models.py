from pydantic import BaseModel


class Expense(BaseModel):
    expense: str
    amount: float
    category: str

class ExpenseOut(BaseModel):
    id: int
    expense: str
    amount: float
    category: str
    date: str

