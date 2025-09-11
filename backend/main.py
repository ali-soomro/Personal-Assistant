"""FastAPI backend entrypoint for Personal Assistant MVP."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.router import route_intent
from backend import apps_macos

from backend.settings import PROTECTED, CATEGORIES

# # System/critical processes we must never close
# PROTECTED: set[str] = {"Finder", "WindowServer", "SystemUIServer", "loginwindow"}

# # Categories supported by the classifier
# CATEGORIES: set[str] = {"coding", "gaming", "browsers", "chat", "media"}

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
    """
    Handle a user query by routing to the correct intent.
    Implements a dry-run for close_apps with dynamic classification via Ollama.
    """
    intent = route_intent(q.user_input)

    if intent == "close_apps":
        text = q.user_input.lower()

        # 1) Which apps are visible right now?
        running = apps_macos.list_apps()

        # 2) Classify each app into a category (cached inside apps_macos)
        classified = {app: apps_macos.classify_app(app) for app in running}

        # 3) Parse: category to close? apps to keep?
        target_cat = next((c for c in CATEGORIES if c in text), None)
        keep = set(PROTECTED)

        if "except" in text:
            # Case 1: "close everything except <app>"
            # Case 3: "close everything except <category>"
            except_cat = next((c for c in CATEGORIES if c in text), None)
            if except_cat:
                # keep the whole category
                keep |= {app for app, cat in classified.items() if cat == except_cat}
            else:
                # keep explicitly mentioned apps
                keep |= {app for app in running if app.lower() in text}

            to_close = [app for app in running if app not in keep]

        elif target_cat:
            # Case 2: "close every <category> app"
            to_close = [
                app for app, cat in classified.items()
                if cat == target_cat and app not in keep
            ]

        else:
            # Default: close everything except protected
            to_close = [app for app in running if app not in keep]

        # Return structured JSON (not one big string)
        return {
            "intent": intent,
            "classified": classified,
            "keeping": sorted(keep),
            "closing": to_close,
            "note": "Dry-run",
        }

    # Default stub for other intents
    return {"intent": intent, "response": f"Stub for intent: {intent}"}