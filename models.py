from pydantic import BaseModel, Field
from typing import Optional

class Expense(BaseModel):
    expense: str = Field(min_length=1, max_length=10)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=10)

class ExpenseOut(BaseModel):
    id: int
    expense: str
    amount: float
    category: str
    date: Optional[str] = None

class User(BaseModel):
    username: str
    password: str

class ExpenseListResponse(BaseModel):
    data: list[ExpenseOut]
    count: int
