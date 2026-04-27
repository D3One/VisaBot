from fastapi import APIRouter, HTTPException, status

from app.models import ApplyResponse, SchengenApplyRequest, StatusResponse
from app.services.schengen_service import submit_schengen_dry_run
from app.services.store import StatusStore
from utils.telegram import send_telegram_message

router = APIRouter(prefix="/api/v1/schengen", tags=["Schengen"])


@router.post("/apply", response_model=ApplyResponse, status_code=status.HTTP_201_CREATED)
async def apply_schengen(payload: SchengenApplyRequest) -> ApplyResponse:
    """Create a local dry-run Schengen application draft."""

    return await submit_schengen_dry_run(payload)


@router.get("/status/{application_number}", response_model=StatusResponse)
async def get_schengen_status(application_number: str) -> StatusResponse:
    """Return locally stored dry-run status and optionally notify Telegram."""

    record = StatusStore().get(application_number)
    if not record or record.get("kind") != "schengen":
        raise HTTPException(status_code=404, detail="Application number not found")

    notified = await send_telegram_message(
        f"Schengen dry-run status\nApplication: {application_number}\nStatus: {record.get('status')}"
    )
    return StatusResponse(
        application_number=application_number,
        status=record.get("status", "UNKNOWN"),
        user_id=record.get("user_id"),
        updated_at=record.get("updated_at"),
        notified=notified,
        note="Local dry-run status only. No external portal was queried.",
    )
