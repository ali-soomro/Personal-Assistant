# Personal AI Assistant – Plan

## Vision
A local-first, privacy-preserving AI assistant running entirely on macOS (M3 Air),
capable of email summarisation, contact/birthday reminders, scheduling,
application management, and workspace organisation. Future: web/voice frontends.

## Goals (MVP)
- [ ] Intent router (rule-based + small LLM fallback)
- [ ] Tool: email summary ("most important email today")
- [ ] Tool: close apps unrelated to coding
- [ ] CLI frontend

## Phase 2
- [ ] Contacts + birthday reminders (WhatsApp drafts)
- [ ] Create schedule from emails
- [ ] Memory (preferences, history)
- [ ] Web dashboard frontend

## Phase 3
- [ ] Move apps into workspaces
- [ ] Voice integration (STT + TTS)
- [ ] More robust RAG & task planning
- [ ] Multi-agent specialisation

## Architecture Overview
- **Frontend**: CLI first, then web, then voice.
- **Backend**: FastAPI orchestrator with plan–act–reflect loop.
- **Models**: local (Ollama/llama.cpp), small router + larger assistant.
- **Tools**: OS/email/contacts/calendar as structured modules.
- **Memory**: SQLite for prefs + lightweight vector store.

## Principles
- Local-first, no cloud dependency.
- Explicit confirmation for destructive actions.
- Modular tools, swappable models.
- Incremental development: working MVP as early as possible.
