from __future__ import annotations

import datetime as dt
import threading
import uuid
from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator

router = APIRouter(prefix="/api/v1/mock", tags=["Mock API"])

# In-memory development storage.
# This is intentionally non-persistent and is reset when the process restarts.
FAKE_DB: dict[str, dict[str, Any]] = {}

AUTO_APPROVE_AFTER_SECONDS = 60


def _generate_app_number(prefix: str) -> str:
    """Generate a pseudo application number: PREFIX + 8-char UUID fragment."""

    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"


def _mark_approved(application_number: str) -> None:
    """Switch a mock application to APPROVED."""

    if application_number in FAKE_DB:
        FAKE_DB[application_number]["status"] = "APPROVED"
        FAKE_DB[application_number]["updated_at"] = dt.datetime.now(dt.timezone.utc)


def _schedule_auto_approve(application_number: str) -> None:
    """Schedule non-blocking status transition for local development."""

    timer = threading.Timer(AUTO_APPROVE_AFTER_SECONDS, _mark_approved, args=(application_number,))
    timer.daemon = True
    timer.start()


class USVisaMockRequest(BaseModel):
    """Mock payload for local US visa endpoint tests."""

    user_id: str = Field(..., description="ID пользователя в вашем боте")
    chat_id: int = Field(..., description="Telegram chat_id для уведомлений")
    surname: str
    given_name: str
    passport_number: str
    birth_date: str = Field(..., description="YYYY-MM-DD")
    arrival_date: str = Field(..., description="YYYY-MM-DD")
    stay_length: str = Field(..., description="Количество дней")
    purpose: Literal["tourism", "business", "study"] = "tourism"

    @field_validator("birth_date", "arrival_date")
    @classmethod
    def validate_date(cls, value: str) -> str:
        try:
            dt.datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD") from exc
        return value

    @field_validator("passport_number")
    @classmethod
    def validate_passport_number(cls, value: str) -> str:
        if not (6 <= len(value) <= 9) or not value.isalnum():
            raise ValueError("Номер паспорта должен содержать 6-9 букв/цифр")
        return value


class SchengenMockRequest(BaseModel):
    """Mock payload for local Schengen endpoint tests."""

    user_id: str
    chat_id: int
    target_country: Literal["germany", "france"]
    surname: str
    given_name: str
    passport_number: str
    birth_date: str
    nationality: str | None = None
    passport_issuing_country: str | None = None
    passport_expiration: str | None = None
    address: str
    city: str
    zip_code: str
    country: str | None = None
    phone: str
    email: EmailStr
    purpose: Literal["tourism", "business", "study", "family"] = "tourism"
    arrival_date: str
    stay_length: str
    occupation: str | None = None

    @field_validator("birth_date", "passport_expiration", "arrival_date")
    @classmethod
    def validate_date(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            dt.datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD") from exc
        return value

    @field_validator("passport_number")
    @classmethod
    def validate_passport_number(cls, value: str) -> str:
        if not (6 <= len(value) <= 9) or not value.isalnum():
            raise ValueError("Номер паспорта должен содержать 6-9 букв/цифр")
        return value


@router.post("/us-visa/apply")
async def mock_us_visa_apply(req: USVisaMockRequest) -> dict[str, str]:
    """Create an in-memory mock US visa application."""

    application_number = _generate_app_number("US")
    now = dt.datetime.now(dt.timezone.utc)
    FAKE_DB[application_number] = {
        "type": "US",
        "status": "PENDING",
        "created_at": now,
        "updated_at": now,
        "payload": req.model_dump(),
    }
    _schedule_auto_approve(application_number)
    return {"application_number": application_number, "status": "PENDING"}


@router.post("/schengen/apply")
async def mock_schengen_apply(req: SchengenMockRequest) -> dict[str, str]:
    """Create an in-memory mock Schengen application."""

    prefix = "DE" if req.target_country == "germany" else "FR"
    application_number = _generate_app_number(prefix)
    now = dt.datetime.now(dt.timezone.utc)
    FAKE_DB[application_number] = {
        "type": "SCHENGEN",
        "status": "PENDING",
        "created_at": now,
        "updated_at": now,
        "payload": req.model_dump(),
    }
    _schedule_auto_approve(application_number)
    return {"application_number": application_number, "status": "PENDING"}


@router.get("/status/{application_number}")
async def mock_get_status(application_number: str) -> dict[str, str]:
    """Return status for an in-memory mock application."""

    record = FAKE_DB.get(application_number)
    if not record:
        raise HTTPException(status_code=404, detail="Заявка не найдена")

    return {
        "application_number": application_number,
        "type": record["type"],
        "status": record["status"],
        "created_at": record["created_at"].isoformat().replace("+00:00", "Z"),
        "updated_at": record["updated_at"].isoformat().replace("+00:00", "Z"),
    }
