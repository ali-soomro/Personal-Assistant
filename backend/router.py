"""LLM-based intent router using Ollama."""

import ollama

INTENTS = [
    "close_apps",
    "email_summary",
    "birthdays",
    "schedule_from_email",
    "move_apps",
    "general",
]


def route_intent(user_input: str) -> str:
    """
    Classify user input into one of the supported intents using a local LLM.
    Falls back to 'general' if the model response is invalid.
    """
    prompt = f"""
    You are an intent classifier.
    Possible intents: {", ".join(INTENTS)}.
    Classify this user input into exactly one of the intents.
    Reply with only the intent key, nothing else.

    User input: "{user_input}"
    """

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}],
    )

    intent = response["message"]["content"].strip().lower()
    if intent not in INTENTS:
        return "general"
    return intent