# Personal AI Assistant – Development Plan

## 🎯 Vision
A local-first, privacy-preserving AI assistant running entirely on a MacBook Air (M3, no dedicated GPU).  
The assistant will be able to read and prioritise email, manage contacts/birthdays, generate schedules, control applications, and eventually integrate with workspaces and voice interfaces.

---

## 🛠️ Principles
- **Local-first**: all models run locally (Ollama / llama.cpp).
- **Privacy by design**: no cloud processing of personal data.
- **Safety first**: explicit confirmation for any destructive action (closing/killing apps, sending messages).
- **Modular**: backend, frontend, and tools are independent and swappable.
- **Incremental delivery**: small, working MVPs at every stage.

---

## 📌 Phase 1 – MVP
Goal: A working backend + CLI frontend that can route intents and perform 1–2 real tasks.

- [ ] **Backend**: FastAPI with `/query` endpoint (accepts user command → returns structured plan/response).
- [ ] **Frontend**: Simple CLI REPL that sends queries to the backend.
- [ ] **Router**: rule-based intent classifier with LLM fallback.
- [ ] **Tool 1**: Email summarisation  
  - Fetch today’s emails via IMAP.  
  - Rank and summarise, output the most important.  
- [ ] **Tool 2**: Close applications unrelated to “coding” (via AppleScript/psutil).
- [ ] **Docs**: PLAN.md + ARCHITECTURE.md with updated diagrams.

---

## 📌 Phase 2 – Useful Assistant
Goal: Broader task coverage and early personalisation.

- [ ] **Contacts/Birthdays**: read from local CSV/VCF, identify today’s birthdays, draft WhatsApp messages (prefilled).
- [ ] **Scheduling**: parse emails → extract tasks/events → propose a daily agenda.
- [ ] **Memory**: store preferences (e.g. “always keep VSCode open”), task history, and outcomes.
- [ ] **Web Frontend**: simple dashboard to view tasks, confirm actions.

---

## 📌 Phase 3 – Power User
Goal: Workspace organisation and richer interfaces.

- [ ] **App Management**: classify apps into categories (coding, gaming, media) and move them to appropriate workspaces.  
- [ ] **Workspace Control**: integrate yabai/skhd (optional, advanced).  
- [ ] **Voice I/O**:  
  - Speech-to-text (Whisper small.en locally).  
  - Text-to-speech (macOS `say` or Coqui TTS).  
- [ ] **Improved Planning**: Plan–Act–Reflect loop with post-execution verification.  

---

## 📌 Phase 4 – Polish & Extensibility
Goal: Turn into a robust framework for daily use.

- [ ] **RAG (Retrieval-Augmented Generation)** for local documents.  
- [ ] **Plugin system** for adding new tools.  
- [ ] **Tests**: integration tests for key flows (email summary, close apps, birthdays).  
- [ ] **Deployment**: make installable on a fresh Mac (script or Homebrew formula).

---

## ✅ Success Criteria
- The assistant runs **fully locally** on an M3 Air.  
- It can correctly identify and execute the 5 core tasks:  
  1. Summarise most important email today.  
  2. Handle birthdays and prepare wishes.  
  3. Build a schedule from email tasks.  
  4. Close unrelated applications safely.  
  5. Move apps into workspaces.  
- User experience is clear, with confirmation prompts for risky actions.  
- Easy to extend with new tools or frontends.
