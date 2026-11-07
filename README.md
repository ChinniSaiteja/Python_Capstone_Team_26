# Python_Capstone_Team_26
# AI-powered Waste Sorting & Recycling Assistant

## Homework Assignment 3 – Waste Management Web App (Flask + MySQL)

#### Project Structure

<img width="662" height="396" alt="image" src="https://github.com/user-attachments/assets/24c4823d-1e15-4786-9e63-f36e16cb8540" />

#### How it works

#### 1) MySQL database
The `waste_management` database contains a `waste_items` table with the waste-item records.

#### 2) Flask application
`database.py` reads the connection settings from the `.env` file, connects to MySQL with `mysql-connector-python`, and retrieves all rows from `waste_items`. `app.py` calls this function in the `/` route.

#### 3) Webpage
The records are passed to `templates/index.html`, which displays them in an HTML table styled by `static/style.css`.

<img width="660" height="110" alt="image" src="https://github.com/user-attachments/assets/9e7473f9-bdca-430d-a4d7-b017295c7563" />

#### Requirements

1. Python 3.12
2. MySQL Server 8.x (and optionally MySQL Workbench)
3. Python packages listed in `requirement.txt`:
   - Flask
   - mysql-connector-python
   - python-dotenv
   - pytest

---

## Homework Assignment 4 – Error Handling and Automated Testing

### Objective

Homework Assignment 4 focuses on error handling and automated testing in the Flask application.

The application was extended with custom exceptions, database error handling, Flask error handlers, and automated tests.

### Error Handling

A dedicated `exceptions.py` module was added for application-specific exceptions.

The exception hierarchy includes:

- `WebInterfaceError`
  - `InvalidRequestError`
- `DatabaseError`
  - `DatabaseConnectionError`
  - `DatabaseQueryError`

The database layer catches MySQL connection and query errors and converts them into application-specific exceptions.

### Flask Error Handlers

`app.py` contains Flask error handlers for:

1. Database-related errors
2. Unexpected application errors

When a database error occurs, the application displays a user-friendly error page instead of exposing the technical database error.

The error page is located at:

```text
Hometaskassignment3/templates/error.html
```

### Automated Testing

The project uses `pytest` for automated testing.

The tests cover:

- Custom exception inheritance
- Successful database connections
- Database connection failures
- Successful database queries
- Database query failures
- Flask application initialization
- Home page availability
- Display of waste items
- Database error handling
- Unexpected error handling
- Integration between the Flask application and error-handling layer

A total of **15 automated tests** were implemented.

### Running the Tests

From the project root, run:

```bash
python -m pytest -v
```

Expected result:

```text
15 passed
```

### Hometask 4 Test Structure

```text
tests/
├── test_app.py
├── test_database.py
├── test_exceptions.py
└── test_integration.py
```

### Hometask 4 Project Structure

```text
Hometaskassignment3/
├── Static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── error.html
├── __init__.py
├── app.py
├── database.py
├── exceptions.py
├── requirement.txt
└── schema.sql

tests/
├── test_app.py
├── test_database.py
├── test_exceptions.py
└── test_integration.py

pytest.ini
README.md
```