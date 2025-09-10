# Personal AI Assistant

Local-first, privacy-preserving assistant running on macOS (M3).

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone git@github.com:ali-soomro/Personal-Assistant.git
cd Personal-Assistant
```

### 2. Setup environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run backend
```bash
uvicorn backend.main:app --reload
```
Visit http://127.0.0.1:8000/ping

### 4. Run CLI
```bash
python3 frontend/cli.py
```
