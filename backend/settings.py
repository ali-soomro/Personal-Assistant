"""Centralised settings for models and constants (local-first)."""
from __future__ import annotations
import os

# ---- Ollama model selection
MODEL_CLASSIFIER = "gemma3:12b"

# ---- Categories & Safety --------------------
CATEGORIES: set[str] = {"coding", "gaming", "browsers", "chat", "media"}
PROTECTED: set[str] = {
    "Finder", "WindowServer", "SystemUIServer", "loginwindow",
    "Terminal", "iTerm2",
}

# ---- Aliases --------------
APP_NAME_ALIASES: dict[str, str] = {
    "Electron": "coding",
    "sublime_text": "coding",
    "google chrome": "browsers",
    "firefox": "browsers",
    "discord": "chat",
    "ChatGPT": "chat",
}