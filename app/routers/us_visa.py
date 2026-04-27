from fastapi import APIRouter, HTTPException, status

from app.models import ApplyResponse, StatusResponse, USVisaApplyRequest
from app.services.store import StatusStore
from app.services.us_visa_service import submit_us_visa_dry_run
from utils.telegram import send_telegram_message

router = APIRouter(prefix="/api/v1/us-visa", tags=["US visa"])


@router.post("/apply", response_model=ApplyResponse, status_code=status.HTTP_201_CREATED)
async def apply_us_visa(payload: USVisaApplyRequest) -> ApplyResponse:
    """Create a local dry-run US visa application draft."""

    return await submit_us_visa_dry_run(payload)


@router.get("/status/{application_number}", response_model=StatusResponse)
async def get_us_visa_status(application_number: str) -> StatusResponse:
    """Return locally stored dry-run status and optionally notify Telegram."""

    record = StatusStore().get(application_number)
    if not record or record.get("kind") != "us_visa":
        raise HTTPException(status_code=404, detail="Application number not found")

    notified = await send_telegram_message(
        f"US visa dry-run status\nApplication: {application_number}\nStatus: {record.get('status')}"
    )
    return StatusResponse(
        application_number=application_number,
        status=record.get("status", "UNKNOWN"),
        user_id=record.get("user_id"),
        updated_at=record.get("updated_at"),
        notified=notified,
        note="Local dry-run status only. No external portal was queried.",
    )
