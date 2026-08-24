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
```

## Deploying to Render

1. Push your repository to GitHub.
2. Sign in to [Render](https://render.com) and click **New +** -> **Web Service**.
3. Connect your GitHub repository (`reeshasayana-commits/Ai-Doctor-Chatbot-`).
4. Configure service settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. In **Environment Variables**, add:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key (`sk-or-v1-...`)
   - `MODEL`: `openai/gpt-4o-mini` (or your preferred model)
   - `FLASK_SECRET_KEY`: A secure random secret string
6. Click **Deploy Web Service**.
