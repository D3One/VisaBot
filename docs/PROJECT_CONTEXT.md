# Project context

The source PDF described a repository named `visa-bot` with a FastAPI API, Docker support, routers for US visa and Schengen workflows, service-layer modules, utility Telegram integration, and Playwright-style scripts.

The PDF also described these public API routes:

- `POST /api/v1/us-visa/apply`
- `GET /api/v1/us-visa/status/{application_number}`
- `POST /api/v1/schengen/apply`
- `GET /api/v1/schengen/status/{application_number}`

This repository preserves that high-level architecture while replacing live browser automation with a dry-run, human-in-the-loop-safe implementation.

## What was intentionally changed

The following behavior is not included:

- automated login to CEAC, VFS, or other visa portals;
- live submission of visa applications;
- CAPTCHA, hCaptcha, Browserless unblock, or anti-bot bypass;
- proxy rotation or evasion logic;
- storage of portal passwords or sensitive credentials.

## Why

Visa and government-adjacent systems usually have strict terms of service, anti-automation controls, and legal/compliance requirements. A repository intended for production should avoid unauthorized automation and should instead use official APIs, human review, and explicit authorization.
