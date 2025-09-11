"""FastAPI backend entrypoint for Personal Assistant MVP."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.router import route_intent
from backend import apps_macos
from backend.settings import PROTECTED


app = FastAPI(title="Personal Assistant MVP")


class Query(BaseModel):
    """Schema for user query payload."""
    user_input: str


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception):
    """Always return JSON on unhandled exceptions so the CLI can parse it."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


@app.get("/ping")
def ping() -> dict[str, str]:
    """Healthcheck endpoint."""
    return {"status": "ok", "message": "pong"}


@app.post("/query")
def query(q: Query) -> dict:
    """Handle a user query by routing to the correct intent."""
    parsed = route_intent(q.user_input)
    intent = parsed["intent"]
    mode = parsed.get("mode", "none")
    targets = parsed.get("targets", [])

    # --- Close apps ---
    if intent == "close_apps":
        running = apps_macos.list_apps()
        classified = {app: apps_macos.classify_app(app) for app in running}
        keep = set(PROTECTED)
        to_close: list[str] = []

        if mode == "app":
            # Close all except explicitly mentioned apps
            keep |= {app for app in running if app.lower() in [t.lower() for t in targets]}
            to_close = [app for app in running if app not in keep]

        elif mode == "category":
            # Keep/close apps based on categories
            if targets:
                keep |= {app for app, cat in classified.items() if cat in targets}
            to_close = [app for app in running if app not in keep]

        else:
            # Fallback: close everything except protected
            to_close = [app for app in running if app not in keep]

        return {
            "intent": intent,
            "classified": classified,
            "keeping": sorted(keep),
            "closing": to_close,
            "note": "Dry-run (no apps actually closed yet)",
        }

    # --- Move apps ---
    if intent == "move_apps":
        return {
            "intent": intent,
            "response": f"Would move apps in categories {targets} to new workspaces (stub).",
        }

    # --- Email summary ---
    if intent == "email_summary":
        return {
            "intent": intent,
            "response": "Stub: You received 12 emails today. 2 marked urgent.",
        }

    # --- Birthdays ---
    if intent == "birthdays":
        return {
            "intent": intent,
            "response": "Stub: Today is Alice's birthday 🎉.",
        }

    # --- Schedule from email ---
    if intent == "schedule_from_email":
        return {
            "intent": intent,
            "response": "Stub: Your schedule is 10am Meeting, 1pm Lunch, 3pm Review.",
        }

    # --- Default fallback ---
    return {"intent": intent, "response": f"Stub for intent: {intent}"}