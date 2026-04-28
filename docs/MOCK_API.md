# Mock API for Local Development

This project includes a safe mock API for testing request validation, Telegram bot payloads, and status polling without contacting any real visa, embassy, CEAC, VFS, CAPTCHA, proxy, or anti-bot service.

## Routes

```text
POST /api/v1/mock/us-visa/apply
POST /api/v1/mock/schengen/apply
GET  /api/v1/mock/status/{application_number}
```

## Behavior

- The mock router stores applications in memory in `FAKE_DB`.
- A new request starts with `PENDING`.
- A background task changes status to `APPROVED` after about 60 seconds.
- Data disappears after an application/container restart.
- Invalid payloads return FastAPI/Pydantic `422 Unprocessable Entity`.

## US Visa Mock Payload

```json
{
  "user_id": "test_user_1",
  "chat_id": 987654321,
  "surname": "Doe",
  "given_name": "John",
  "passport_number": "A1234567",
  "birth_date": "1990-01-01",
  "arrival_date": "2026-07-15",
  "stay_length": "30",
  "purpose": "tourism"
}
```

## Schengen Mock Payload

```json
{
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
}
```

## Status Check

```bash
curl http://localhost:8000/api/v1/mock/status/US3F9E7A2B
```

Expected response:

```json
{
  "application_number": "US3F9E7A2B",
  "type": "US",
  "status": "PENDING",
  "created_at": "2026-04-28T18:00:00Z",
  "updated_at": "2026-04-28T18:00:00Z"
}
```
