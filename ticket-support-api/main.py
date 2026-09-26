"""
main.py
-------
The FastAPI application: defines all endpoints and the business-logic
helper function required by the assignment.
"""

from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse

from database import get_db_connection, init_db
from models import TicketCreate, TicketResponse, TicketStatus

app = FastAPI(title="Customer Support Ticket API")


@app.on_event("startup")
def on_startup():
    """Runs once when the server starts. Makes sure the table exists."""
    init_db()


# ---------------------------------------------------------------------
# Business logic: response deadline calculation
# ---------------------------------------------------------------------
def calculate_response_deadline(created_at: datetime) -> datetime:
    """
    Returns the datetime exactly 3 *business* days (Mon-Fri) after
    `created_at`, using only the standard library `datetime` module.

    Logic: start from created_at and step forward one calendar day at a
    time. Every time we land on a weekday (Mon=0 ... Fri=4), we count it
    as one business day. We stop once we've counted 3 such days.
    Weekend days (Sat=5, Sun=6) are skipped and not counted.
    """
    days_added = 0
    current_date = created_at
    while days_added < 3:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday(0) to Friday(4)
            days_added += 1
    return current_date


# ---------------------------------------------------------------------
# Helper: convert a raw sqlite3.Row into a TicketResponse
# ---------------------------------------------------------------------
def row_to_response(row) -> TicketResponse:
    created_at = datetime.fromisoformat(row["created_at"])
    return TicketResponse(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        status=row["status"],
        tags=row["tags"],
        created_at=created_at,
        response_deadline=calculate_response_deadline(created_at),
    )


# ---------------------------------------------------------------------
# POST /tickets - create a ticket, returns JSON
# ---------------------------------------------------------------------
@app.post("/tickets", response_model=TicketResponse, status_code=201)
def create_ticket(ticket: TicketCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now()

    cursor.execute(
        """
        INSERT INTO tickets (title, description, status, tags, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (ticket.title, ticket.description, ticket.status, ticket.tags, created_at.isoformat()),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return TicketResponse(
        id=new_id,
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
        tags=ticket.tags,
        created_at=created_at,
        response_deadline=calculate_response_deadline(created_at),
    )


# ---------------------------------------------------------------------
# GET /tickets - list all tickets, returns JSON array
# ---------------------------------------------------------------------
@app.get("/tickets", response_model=List[TicketResponse])
def list_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_response(row) for row in rows]


# ---------------------------------------------------------------------
# GET /tickets/{id} - a single ticket, returns JSON
# ---------------------------------------------------------------------
@app.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return row_to_response(row)


# ---------------------------------------------------------------------
# POST /tickets/web-submit - legacy form endpoint, returns raw HTML
# ---------------------------------------------------------------------
@app.post("/tickets/web-submit", response_class=HTMLResponse)
def web_submit_ticket(
    title: str = Form(...),
    description: str = Form(...),
    status: TicketStatus = Form("Open"),
    tags: str = Form(""),
):
    """
    Simulates an old-school HTML <form> POST (application/x-www-form-urlencoded),
    not JSON. FastAPI's Form(...) reads fields the same way it would read
    form-data submitted by a browser <form>.
    Per the spec, this endpoint must NOT return JSON — it returns a raw
    HTML string instead.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now()
    cursor.execute(
        """
        INSERT INTO tickets (title, description, status, tags, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, description, status, tags, created_at.isoformat()),
    )
    conn.commit()
    conn.close()

    return "<h1>Ticket Created Successfully!</h1>"
