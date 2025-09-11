"""macOS application management tools for Personal Assistant."""

import subprocess
import os
import signal
from typing import List
import ollama
import psutil

from backend.settings import MODEL_CLASSIFIER

# Cache for app classifications to avoid repeated LLM calls
_APP_CLASS_CACHE: dict[str, str] = {}


def list_apps() -> List[str]:
    """Return a list of visible (non-background) applications."""
    script = 'tell application "System Events" to get name of (processes where background only is false)'
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        check=True,
    )
    apps = result.stdout.strip().split(", ")
    return apps


def classify_app(app_name: str) -> str:
    """
    Use Ollama to classify an app into a category.
    Categories: coding, gaming, browsers, chat, media, other.
    """
    categories = ["coding", "gaming", "browsers", "chat", "media", "other"]

    if app_name in _APP_CLASS_CACHE:
        return _APP_CLASS_CACHE[app_name]

    prompt = f"""
    Classify this macOS application into exactly one of the following categories:
    - coding (e.g., Visual Studio Code, sublime_text, PyCharm, Xcode, IntelliJ, Terminal)
    - gaming (e.g., Steam, Riot Client, Epic Games, Minecraft)
    - browsers (e.g., Safari, Firefox, Google Chrome, Brave)
    - chat (e.g., Discord, Slack, Telegram, WhatsApp, ChatGPT)
    - media (e.g., Spotify, VLC, Music, Photos)
    - other (everything else)

    Application: "{app_name}"

    Reply with only the category name.
    """

    try:
        response = ollama.chat(
            model=MODEL_CLASSIFIER,
            messages=[{"role": "user", "content": prompt}],
        )
        category = response["message"]["content"].strip().lower()
    except Exception:
        category = "other"

    if category not in categories:
        category = "other"

    _APP_CLASS_CACHE[app_name] = category
    return category


def close_app(app_name: str) -> bool:
    """Try to gracefully quit an application by name. Fallback to kill if needed."""
    try:
        # Try AppleScript quit
        subprocess.run(
            ["osascript", "-e", f'tell application "{app_name}" to quit'],
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        # Fallback: find PID and terminate
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] and app_name.lower() in proc.info["name"].lower():
                try:
                    os.kill(proc.info["pid"], signal.SIGTERM)
                    return True
                except OSError:
                    try:
                        os.kill(proc.info["pid"], signal.SIGKILL)
                        return True
                    except OSError:
                        return False
    return False


def close_apps(apps: List[str]) -> dict:
    """Close multiple apps by name and return results."""
    results = {}
    for app in apps:
        results[app] = close_app(app)
    return results