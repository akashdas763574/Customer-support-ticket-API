"""
models.py
---------
Pydantic models define the *shape* of data going in and out of the API.
FastAPI uses these to:
  1. Validate incoming JSON (reject bad requests automatically).
  2. Auto-generate the OpenAPI/Swagger docs.
  3. Serialize outgoing responses to JSON.
"""

from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel

# The PDF spec defines status as one of exactly these 3 values.
# Literal[...] makes Pydantic reject anything else with a 422 error.
TicketStatus = Literal["Open", "In Progress", "Closed"]


class TicketCreate(BaseModel):
    """What the client must send in the body of POST /tickets."""
    title: str
    description: str
    status: Optional[TicketStatus] = "Open"   # defaults to "Open" if not supplied
    tags: Optional[str] = ""                  # comma-separated string, e.g. "billing,urgent"


class TicketResponse(BaseModel):
    """What the API sends back for a single ticket."""
    id: int
    title: str
    description: str
    status: str
    tags: str
    created_at: datetime
    response_deadline: datetime      # computed, not stored in the DB
