# Telegram Bot Data Collection Fields

This document defines the user data that the Telegram bot should collect before sending a JSON payload to the FastAPI backend.

> Safety note: collect only the data needed for the requested workflow, protect it as sensitive personal data, and do not use this backend to bypass CAPTCHA, anti-bot controls, or visa-provider terms. The current repository is a safe dry-run scaffold and does not submit applications to external visa portals.

## Recommended placement

Place this file in:

```text
docs/TELEGRAM_BOT_DATA_FIELDS.md
```

This keeps product/legal/operational documentation separate from executable code.

---

## Field table for the Telegram bot

| Field | Required for US visa dry-run | Required for Schengen dry-run | Description | Format / Allowed values | Example |
|---|---:|---:|---|---|---|
| `user_id` | Yes | Yes | Unique user identifier in your bot. | String or numeric string | `12345` |
| `chat_id` | Yes | Yes | Telegram chat ID where backend notifications should be sent. This is now passed in each API request, not stored in `.env`. | Integer; private chats are usually positive, groups may be negative | `987654321` |
| `surname` | Yes | Yes | Applicant surname / family name in Latin characters. | String | `Miller` |
| `given_name` | Yes | Yes | Applicant given name in Latin characters. | String | `Anna` |
| `other_names` | No | No | Patronymic, middle name, or other names, if relevant. | String | `Petrovich` |
| `birth_date` | Yes | Yes | Date of birth. | `YYYY-MM-DD` | `1992-05-12` |
| `nationality` | Optional | Optional | Citizenship / nationality country code. | ISO-3166 alpha-2 country code | `DE`, `RU` |
| `passport_number` | Yes | Yes | International passport number. | Latin letters and digits | `C1234567` |
| `passport_issuing_country` | Optional | Optional | Country that issued the passport. | ISO-3166 alpha-2 country code | `DE` |
| `passport_expiration` | Optional | Optional | Passport expiration date. | `YYYY-MM-DD` | `2030-12-31` |
| `address` | No | Yes | Residential or mailing street address. | String | `Musterstrasse 12` |
| `city` | No | Yes | City of residence. | String | `Berlin` |
| `zip_code` | No | Yes | Postal code. | String | `10115` |
| `country` | No | Optional | Country of residence. | ISO-3166 alpha-2 country code | `DE` |
| `phone` | No | Yes | Phone number with international dialing code. | E.164-style string preferred | `+4915112345678` |
| `email` | No | Yes | Contact email address. | Valid email | `anna.mueller@example.com` |
| `purpose` | Yes | Yes | Purpose of travel. | `tourism`, `business`, `study`, `family`, `other` | `tourism` |
| `arrival_date` | Yes | Yes | Planned arrival date. | `YYYY-MM-DD` | `2026-09-15` |
| `stay_length` | Yes | Yes | Planned stay length in days. | Integer, `1`-`365` | `14` |
| `occupation` | No | Optional | Profession or current status. | String, for example `student`, `employee`, `unemployed` | `student` |
| `target_country` | No | Yes | Target Schengen country handled by the backend. | `germany` or `france` | `germany` |

---

## Important Telegram notification note

The backend no longer reads a global `TELEGRAM_CHAT_ID` from `.env`.

The bot should include `chat_id` in every `POST /api/v1/us-visa/apply` and `POST /api/v1/schengen/apply` request. The backend stores that value with the local dry-run record and reuses it for later status notifications.

`.env` should contain only the bot token:

```env
BOT_TOKEN=123456:ABCDEF
```

---

## Important API naming note

The backend Schengen model now accepts the postal code as `zip_code`, matching the Telegram bot collection table and the patch instructions.

---

## Minimal US visa dry-run payload

```json
{
  "user_id": "12345",
  "chat_id": 987654321,
  "surname": "Miller",
  "given_name": "Anna",
  "passport_number": "C1234567",
  "birth_date": "1992-05-12",
  "arrival_date": "2026-09-15",
  "stay_length": 30,
  "purpose": "tourism"
}
```

Optional US fields currently supported by the backend model:

```json
{
  "sex": "F",
  "citizenship_country": "DE",
  "passport_issuing_country": "DE",
  "passport_expiration": "2030-12-31"
}
```

---

## Minimal Schengen dry-run payload

```json
{
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
}
```

Optional Schengen fields currently supported by the backend model:

```json
{
  "nationality": "DE",
  "passport_issuing_country": "DE",
  "passport_expiration": "2030-12-31",
  "country": "DE",
  "occupation": "student"
}
```

---

## Suggested Telegram bot question flow

1. Ask which workflow the user needs: `us_visa` or `schengen`.
2. Capture Telegram identifiers from the bot context:
   - `user_id`
   - `chat_id`
3. Collect the common fields:
   - `surname`
   - `given_name`
   - `other_names`, if applicable
   - `birth_date`
   - `nationality`
   - `passport_number`
   - `passport_issuing_country`
   - `passport_expiration`
   - `purpose`
   - `arrival_date`
   - `stay_length`
4. For Schengen, additionally collect:
   - `target_country`
   - `address`
   - `city`
   - `zip_code`
   - `country`
   - `phone`
   - `email`
   - `occupation`
5. Show a confirmation summary to the user before sending anything to the backend.
6. Convert the collected data into the backend JSON payload.
7. Send the payload to:
   - `POST /api/v1/us-visa/apply`, or
   - `POST /api/v1/schengen/apply`.
8. Save the returned `application_number` together with `user_id` and `chat_id` in your bot database.

---

## Basic validation rules for the bot

| Field type | Validation rule |
|---|---|
| Dates | Must match `YYYY-MM-DD`; reject impossible calendar dates. |
| Email | Must contain a valid email format before sending to backend. |
| Phone | Prefer international format with `+` and country code. |
| Country codes | Use ISO-3166 alpha-2 codes, for example `DE`, `RU`, `US`. |
| `purpose` | Restrict to `tourism`, `business`, `study`, `family`, `other`. |
| `target_country` | Restrict to `germany` or `france` unless backend support is expanded. |
| `stay_length` | Positive integer; current backend model allows `1`-`365`. |
| `chat_id` | Must be numeric; private chat IDs are usually positive, group/supergroup IDs may be negative. |

---

## Security and privacy notes for the colleague

- Treat passport number, date of birth, address, phone, and email as sensitive personal data.
- Do not log full passport numbers in application logs.
- Mask sensitive values in bot admin panels, for example `C12****67`.
- Store only `BOT_TOKEN` in `.env`; pass `chat_id` in the request payload.
- Encrypt secrets in `.env` or secret manager; do not commit real tokens to GitHub.
- Store only what is needed and define a retention period.
- Add a user confirmation step before creating any backend draft.
- Add a deletion/export process if users ask to remove or review their stored data.
