from fastapi import APIRouter, HTTPException, status

from app.models import ApplyResponse, SchengenApplyRequest, StatusResponse
from app.services.schengen_service import submit_schengen_dry_run
from app.services.store import StatusStore
from utils.telegram import send_telegram_message

router = APIRouter(prefix="/api/v1/schengen", tags=["Schengen"])


@router.post("/apply", response_model=ApplyResponse, status_code=status.HTTP_201_CREATED)
async def apply_schengen(payload: SchengenApplyRequest) -> ApplyResponse:
    """Create a local dry-run Schengen application draft."""

    await send_telegram_message(
        payload.chat_id,
        f"🚀 Schengen dry-run started for user <b>{payload.user_id}</b> ({payload.target_country}).",
    )

    try:
        result = await submit_schengen_dry_run(payload)
    except Exception as exc:
        await send_telegram_message(
            payload.chat_id,
            f"❗️Schengen dry-run failed for user <b>{payload.user_id}</b>: {exc}",
        )
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    await send_telegram_message(
        payload.chat_id,
        f"✅ Schengen dry-run draft created. <b>Application:</b> {result.application_number}",
    )
    return result


@router.get("/status/{application_number}", response_model=StatusResponse)
async def get_schengen_status(application_number: str) -> StatusResponse:
    """Return locally stored dry-run status and optionally notify Telegram."""

    record = StatusStore().get(application_number)
    if not record or record.get("kind") != "schengen":
        raise HTTPException(status_code=404, detail="Application number not found")

    chat_id = record.get("chat_id") or record.get("applicant", {}).get("chat_id")
    notified = await send_telegram_message(
        chat_id,
        f"Schengen dry-run status\nApplication: {application_number}\nStatus: {record.get('status')}",
    )
    return StatusResponse(
        application_number=application_number,
        status=record.get("status", "UNKNOWN"),
        user_id=record.get("user_id"),
        updated_at=record.get("updated_at"),
        notified=notified,
        note="Local dry-run status only. No external portal was queried.",
    )
