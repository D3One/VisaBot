# Legal and operational notes

This project is a safe technical scaffold. It is not legal advice.

## Recommended lawful workflow

1. Collect user-provided information through a Telegram bot, web form, or CRM.
2. Validate required fields through the FastAPI API.
3. Store the draft in your own database with proper encryption and access controls.
4. Let a trained human operator review the data.
5. Submit through official channels, official APIs, or authorized provider workflows only.
6. Keep audit logs, user consent, and data retention policies.

## Data protection checklist

- Encrypt sensitive applicant data at rest.
- Use TLS everywhere.
- Restrict admin access by role.
- Log access to applicant records.
- Never commit `.env` files or credentials.
- Rotate secrets and Telegram bot tokens.
- Add deletion/export flows for user data.
- Use a real database for production.

## Production hardening ideas

- PostgreSQL or MongoDB storage instead of a JSON file.
- Background queue for notifications.
- Structured logging with request IDs.
- Rate limiting.
- Authentication and authorization for API clients.
- Secrets manager integration.
- CI/CD pipeline with linting and tests.
- Docker image scanning.
- SBOM generation.
