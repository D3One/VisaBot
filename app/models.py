from datetime import date, datetime, timezone
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


class VisaApplicantBase(BaseModel):
    user_id: str = Field(..., examples=["987654321"])
    chat_id: int = Field(
        ...,
        description="Telegram chat_id where API notifications should be sent.",
        examples=[987654321],
    )
    surname: str = Field(..., min_length=1, max_length=80, examples=["Miller"])
    given_name: str = Field(..., min_length=1, max_length=80, examples=["Anna"])
    passport_number: str = Field(..., min_length=3, max_length=32, examples=["C1234567"])
    birth_date: date = Field(..., examples=["1992-05-12"])
    arrival_date: date = Field(..., examples=["2026-09-15"])
    stay_length: int = Field(..., ge=1, le=365, examples=[14])
    purpose: str = Field(..., min_length=2, max_length=80, examples=["tourism"])

    @field_validator("surname", "given_name", "passport_number", "purpose")
    @classmethod
    def strip_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class USVisaApplyRequest(VisaApplicantBase):
    """Dry-run payload for a US visa application draft."""

    sex: Literal["M", "F", "X"] | None = Field(default=None, description="Optional applicant sex marker.")
    citizenship_country: str | None = Field(default=None, max_length=2, description="ISO-3166 alpha-2 country code.")
    passport_issuing_country: str | None = Field(default=None, max_length=2, description="ISO-3166 alpha-2 country code.")
    passport_expiration: date | None = None


class SchengenApplyRequest(VisaApplicantBase):
    """Dry-run payload for a Schengen visa application draft."""

    target_country: Literal["germany", "france"] = Field(..., examples=["germany"])
    address: str = Field(..., min_length=2, max_length=200, examples=["Musterstrasse 12"])
    city: str = Field(..., min_length=1, max_length=80, examples=["Berlin"])
    zip_code: str = Field(..., min_length=2, max_length=20, examples=["10115"], description="Postal code.")
    phone: str = Field(..., min_length=6, max_length=32, examples=["+4915112345678"])
    email: EmailStr = Field(..., examples=["anna.mueller@example.com"])

    # The uploaded PDF's Playwright sample referenced these extra fields in code.
    # They are optional here to keep the public API friendly while preserving extensibility.
    nationality: str | None = Field(default=None, max_length=2, description="ISO-3166 alpha-2 country code.")
    passport_issuing_country: str | None = Field(default=None, max_length=2, description="ISO-3166 alpha-2 country code.")
    passport_expiration: date | None = None
    country: str | None = Field(default=None, max_length=2, description="Residence country, ISO-3166 alpha-2.")
    occupation: str | None = Field(default=None, max_length=80)

    @field_validator("address", "city", "zip_code", "phone")
    @classmethod
    def strip_schengen_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be empty")
        return value


class ApplyResponse(BaseModel):
    application_number: str
    status: str
    user_id: str
    created_at: datetime
    screenshot_base64: str | None = None
    pdf_base64: str | None = None
    note: str


class StatusResponse(BaseModel):
    application_number: str
    status: str
    user_id: str | None = None
    updated_at: datetime | None = None
    notified: bool = False
    note: str | None = None


def utc_now() -> datetime:
    return datetime.now(timezone.utc)
