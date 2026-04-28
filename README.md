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
- sends optional Telegram notifications to the `chat_id` provided in each API request;
- exposes `/api/v1/mock/*` endpoints for local development without calling any external visa portal;
- keeps the same overall structure so you can adapt it for lawful, human-in-the-loop workflows.

Use only with official APIs, explicit authorization, and the applicable terms of the relevant visa-processing provider.

## Latest patch: per-request Telegram `chat_id`

Telegram notifications no longer use a global `TELEGRAM_CHAT_ID` from `.env`.

The `.env` file stores only the bot token:

```env
BOT_TOKEN=123456:ABCDEF
```

For backwards compatibility, `TELEGRAM_BOT_TOKEN` is also accepted by the app, but new deployments should use `BOT_TOKEN`.

Every `POST /apply` request must now include:

```json
"chat_id": 987654321
```

This lets the same Docker container notify different Telegram chats without changing environment variables or restarting the container.

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
│  │  ├─ schengen.py
│  │  └─ mock_router.py
│  └─ services/
│     ├─ __init__.py
│     ├─ schengen_service.py
│     ├─ store.py
│     └─ us_visa_service.py
├─ docs/
│  ├─ LEGAL_AND_OPERATIONAL_NOTES.md
│  ├─ PROJECT_CONTEXT.md
│  └─ TELEGRAM_BOT_DATA_FIELDS.md
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
# Edit .env and set BOT_TOKEN if Telegram notifications are needed.
docker compose up --build
```

Open:

```text
http://localhost:8000/docs
```


## Local mock API

The mock API is intended for safe local development. It does not call CEAC, VFS, embassy sites, CAPTCHA services, proxy providers, or any other external visa-processing portal.

Available mock routes:

```text
POST /api/v1/mock/us-visa/apply
POST /api/v1/mock/schengen/apply
GET  /api/v1/mock/status/{application_number}
```

Mock applications are stored in memory in `FAKE_DB`. After roughly 60 seconds, the background task changes the status from `PENDING` to `APPROVED`. The data is reset when the API process or container restarts.

### Mock US visa request

```bash
curl -X POST http://localhost:8000/api/v1/mock/us-visa/apply \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "test_user_1",
    "chat_id": 987654321,
    "surname": "Doe",
    "given_name": "John",
    "passport_number": "A1234567",
    "birth_date": "1990-01-01",
    "arrival_date": "2026-07-15",
    "stay_length": "30",
    "purpose": "tourism"
  }'
```

### Mock status check

```bash
curl http://localhost:8000/api/v1/mock/status/US3F9E7A2B
```

### Mock Schengen request

```bash
curl -X POST http://localhost:8000/api/v1/mock/schengen/apply \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "test_user_2",
    "chat_id": 987654321,
    "target_country": "germany",
    "surname": "Doe",
    "given_name": "Jane",
    "passport_number": "B1234567",
    "birth_date": "1991-02-02",
    "nationality": "DE",
    "passport_issuing_country": "DE",
    "passport_expiration": "2030-12-31",
    "address": "Musterstrasse 12",
    "city": "Berlin",
    "zip_code": "10115",
    "country": "DE",
    "phone": "+4915112345678",
    "email": "jane.doe@example.com",
    "purpose": "tourism",
    "arrival_date": "2026-09-15",
    "stay_length": "14",
    "occupation": "student"
  }'
```

## Example requests

### US visa dry-run application

```bash
curl -X POST http://localhost:8000/api/v1/us-visa/apply \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "12345",
    "chat_id": 987654321,
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
    "chat_id": 987654321,
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
    "zip_code": "10115",
    "phone": "+4915112345678",
    "email": "anna.mueller@example.com"
  }'
```

The Schengen endpoint now uses `zip_code`.

### Status check

```bash
curl http://localhost:8000/api/v1/us-visa/status/US-DRYRUN-20260427-ABC12345
curl http://localhost:8000/api/v1/schengen/status/SCH-DRYRUN-20260427-ABC12345
```

Status notifications use the `chat_id` stored when the corresponding draft was created. For old records created before this patch, Telegram notification will be skipped if no `chat_id` is available.

## Telegram notifications

Set only the bot token in `.env`:

```env
BOT_TOKEN=123456:ABCDEF
```

Then include `chat_id` in each `POST /apply` JSON request. Changing the target Telegram chat no longer requires a Docker restart.

## Development

```bash
pytest -q
```

## How to push to GitHub

```bash
git add .
git commit -m "Require Telegram chat_id per API request"
git push
```
