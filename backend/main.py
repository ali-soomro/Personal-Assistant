"""FastAPI backend entrypoint for Personal Assistant MVP."""

from fastapi import FastAPI
from pydantic import BaseModel

from backend.router import route_intent

app = FastAPI(title="Personal Assistant MVP")


class Query(BaseModel):
    """Schema for user query payload."""
    user_input: str


@app.get("/ping")
def ping() -> dict[str, str]:
    """Healthcheck endpoint."""
    return {"status": "ok", "message": "pong"}


@app.post("/query")
def query(q: Query) -> dict[str, str]:
    """
    Handle a user query by routing to the correct intent.
    Currently returns a stub response.
    """
    intent = route_intent(q.user_input)
    return {"intent": intent, "response": f"Stub for intent: {intent}"}
