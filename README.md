# visa-bot-safe

Safe FastAPI scaffold for a visa-application assistant backend.

This repository was generated from a PDF brief that described a Docker + FastAPI project with these API routes:

- `POST /api/v1/us-visa/apply`
- `GET /api/v1/us-visa/status/{application_number}`
- `POST /api/v1/schengen/apply`
- `GET /api/v1/schengen/status/{application_number}`

## Important safety and compliance note

The original PDF included examples of browser automation for visa portals and references to CAPTCHA/unblock/proxy-style behavior. This repository intentionally does **not** include code that logs into government/visa portals, submits live applications, bypasses CAPTCHA, rotates proxies, or evades anti-bot protections.

Instead, it provides a working, deployable API scaffold that:

- validates applicant data;
- creates local dry-run application records;
- returns placeholder `application_number`, `screenshot_base64`, or `pdf_base64` values;
- stores status in a local JSON file;
- optionally sends Telegram notifications;
- keeps the same overall structure so you can adapt it for lawful, human-in-the-loop workflows.

Use only with official APIs, explicit authorization, and the applicable terms of the relevant visa-processing provider.

## Repository structure

```text
visa-bot-safe/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ models.py
│  ├─ core/
│  │  ├─ __init__.py
│  │  └─ config.py
│  ├─ routers/
│  │  ├─ __init__.py
│  │  ├─ us_visa.py
│  │  └─ schengen.py
│  └─ services/
│     ├─ __init__.py
│     ├─ schengen_service.py
│     ├─ store.py
│     └─ us_visa_service.py
├─ docs/
│  ├─ LEGAL_AND_OPERATIONAL_NOTES.md
│  └─ PROJECT_CONTEXT.md
├─ scripts/
│  ├─ schengen_playwright.py
│  └─ us_visa_playwright.py
├─ tests/
│  └─ test_api.py
├─ utils/
│  ├─ __init__.py
│  └─ telegram.py
├─ .env.example
├─ .gitignore
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md
```

## Quick start: local Python

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## Quick start: Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Open:

```text
http://localhost:8000/docs
```

## Example requests

### US visa dry-run application

```bash
curl -X POST http://localhost:8000/api/v1/us-visa/apply \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345",
    "surname": "Miller",
    "given_name": "Anna",
    "passport_number": "C1234567",
    "birth_date": "1992-05-12",
    "arrival_date": "2026-09-15",
    "stay_length": 30,
    "purpose": "tourism"
  }'
```

### Schengen dry-run application

```bash
curl -X POST http://localhost:8000/api/v1/schengen/apply \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345",
    "target_country": "germany",
    "surname": "Miller",
    "given_name": "Anna",
    "passport_number": "C1234567",
    "birth_date": "1992-05-12",
    "arrival_date": "2026-09-15",
    "stay_length": 14,
    "purpose": "tourism",
    "address": "Musterstrasse 12",
    "city": "Berlin",
    "zip": "10115",
    "phone": "+4915112345678",
    "email": "anna.mueller@example.com"
  }'
```

### Status check

```bash
curl http://localhost:8000/api/v1/us-visa/status/US-DRYRUN-20260427-ABC12345
curl http://localhost:8000/api/v1/schengen/status/SCH-DRYRUN-20260427-ABC12345
```

## Telegram notifications

Set these variables in `.env`:

```env
TELEGRAM_BOT_TOKEN=123456:ABCDEF
TELEGRAM_CHAT_ID=123456789
```

If both variables are present, status checks can send a simple notification.

## Development

```bash
pytest -q
```

## How to push to GitHub

```bash
git init
git add .
git commit -m "Initial safe FastAPI visa assistant scaffold"
git branch -M main
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
git push -u origin main
```
