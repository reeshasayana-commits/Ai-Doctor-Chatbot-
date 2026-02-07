# AI Doctor Chatbot (Demo)

Educational guidance only. Not a diagnosis. For emergencies, call local emergency services.

## Quick Start
```bash
# 1) Create and activate a virtual environment (Windows PowerShell)
python -m venv .venv
. .venv/Scripts/Activate.ps1

# 2) Install deps
pip install -r requirements.txt

# 3) Configure keys
# Option A — use a local .env file (recommended for local dev)
copy .env.example .env
REM Edit `.env` and set your real key for `OPENROUTER_API_KEY` (do NOT commit `.env`).

# Option B — set environment variable system-wide (Windows cmd.exe)
REM Run in cmd.exe (restart terminal after setx):
setx OPENROUTER_API_KEY "sk-your-api-key-here"

# Option C — set environment variable in PowerShell (temporary for session):
$env:OPENROUTER_API_KEY = 'sk-your-api-key-here'

# Notes:
# - The app will load `.env` automatically in development (requires `python-dotenv`, already in `requirements.txt`).
# - For production, prefer setting real environment variables in your hosting platform or CI/CD secrets store.

# 4) Run
python app.py

# 5) Open
http://localhost:5000
