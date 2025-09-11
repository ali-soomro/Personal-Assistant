"""Centralised settings for models and constants (local-first)."""
from __future__ import annotations
import os

# ---- Ollama model selection (override via env vars) -------------------------
# Intent router model
MODEL_INTENT: str = os.getenv("OLLAMA_MODEL_INTENT", "deepseek-r1:8b")
# App classifier model (defaults to the same unless overridden)
MODEL_CLASSIFIER: str = os.getenv("OLLAMA_MODEL_CLASSIFIER", MODEL_INTENT)
# Sampling controls (kept simple)
OLLAMA_TEMPERATURE: float = float(os.getenv("OLLAMA_TEMPERATURE", "0"))

# ---- Categories & Safety ----------------------------------------------------
CATEGORIES: set[str] = {"coding", "gaming", "browsers", "chat", "media"}
PROTECTED: set[str] = {
    "Finder", "WindowServer", "SystemUIServer", "loginwindow",
    # dev/runtime tools you probably never want to close accidentally:
    "Terminal", "iTerm2",
}

# ---- Optional normalisation of process names -> friendly names --------------
APP_NAME_ALIASES: dict[str, str] = {
    "Electron": "Visual Studio Code",
    "sublime_text": "Sublime Text",
    "google chrome": "Google Chrome",
    "firefox": "Firefox",
    "discord": "Discord",
}