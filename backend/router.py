"""LLM-based intent router using Ollama with explicit intent descriptions."""
from __future__ import annotations
import ollama
from backend.settings import MODEL_INTENT  # <-- centralised

INTENTS = [
    "close_apps",
    "email_summary",
    "birthdays",
    "schedule_from_email",
    "move_apps",
    "general",
]

INTENT_DESCRIPTIONS = """
- close_apps: when the user asks to quit, close, or terminate applications, could include or exclude.
- move_apps: when the user asks to rearrange, group, or move applications into workspaces or desktops.
- email_summary: when the user asks about emails, inbox, important or urgent mail.
- birthdays: when the user asks about birthdays, reminders, or sending wishes.
- schedule_from_email: when the user asks to create a schedule or agenda from email.
- general: when the query doesn't match the others.
"""

def route_intent(user_input: str) -> str:
    """Classify user input into one of the supported intents."""
    prompt = f"""
    You are an intent classifier.
    Possible intents: {", ".join(INTENTS)}.

    Descriptions:
    {INTENT_DESCRIPTIONS}

    Classify this user input into exactly one intent.
    Reply with only the intent key.

    User input: "{user_input}"
    """
    try:
        response = ollama.chat(
            model=MODEL_INTENT,                       # <-- use central model
            messages=[{"role": "user", "content": prompt}],
        )
        intent = response["message"]["content"].strip().lower()
    except Exception:
        return "general"

    return intent if intent in INTENTS else "general"