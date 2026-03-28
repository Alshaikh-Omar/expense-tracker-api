# Expense Tracker API

A backend API built with FastAPI and SQLite.

## Features
- Add, edit, delete expenses
- Search expenses
- Pagination (limit, offset)
- Sorting and filtering

## Endpoints
- GET /expenses
- GET /expenses/{id}
- POST /expenses
- PUT /expenses/{id}
- DELETE /expenses/{id}

## Run
uvicorn mainapi:app --reload