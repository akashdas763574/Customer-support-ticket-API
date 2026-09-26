# Customer Support Ticket API

A lightweight Python backend (FastAPI + SQLite) for creating, viewing, and
updating customer support tickets.

## Tech Stack
- **Framework:** FastAPI
- **Database:** SQLite (via the standard `sqlite3` module, no ORM)
- **Server:** Uvicorn (ASGI server)

## Project Structure
```
ticket_api/
├── main.py           # FastAPI app + all endpoints + business logic
├── database.py        # SQLite connection + table creation
├── models.py           # Pydantic request/response schemas
├── requirements.txt
└── README.md
```

## Setup & Run Locally

1. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.
   A `tickets.db` SQLite file will be created automatically in the project
   folder on first run — no manual DB setup needed.

4. **Interactive API docs**
   FastAPI auto-generates Swagger UI at `http://127.0.0.1:8000/docs`,
   where you can try every endpoint from the browser.

## Endpoints

| Method | Path                  | Description                              | Response |
|--------|-----------------------|-------------------------------------------|----------|
| POST   | `/tickets`             | Create a new ticket                       | JSON     |
| GET    | `/tickets`             | List all tickets                          | JSON     |
| GET    | `/tickets/{id}`         | Get a single ticket                       | JSON     |
| POST   | `/tickets/web-submit`   | Legacy form endpoint                      | Raw HTML |

### Example: create a ticket (JSON)
```bash
curl -X POST http://127.0.0.1:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{"title": "Login broken", "description": "Cannot log in", "tags": "billing,urgent"}'
```

### Example: legacy web form submit
```bash
curl -X POST http://127.0.0.1:8000/tickets/web-submit \
  -F "title=Login broken" \
  -F "description=Cannot log in" \
  -F "tags=billing,urgent"
```
Returns: `<h1>Ticket Created Successfully!</h1>`

## Business Logic

`calculate_response_deadline(created_at)` in `main.py` computes a deadline
exactly **3 business days** (Monday–Friday) after ticket creation, using
only Python's built-in `datetime` module — it walks forward one calendar
day at a time and only counts weekdays, skipping Saturday/Sunday.
