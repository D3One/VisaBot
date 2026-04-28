import base64
import secrets
from datetime import datetime, timezone

from app.models import ApplyResponse, USVisaApplyRequest
from app.services.store import StatusStore


# 1x1 transparent PNG. Enough to keep response schema compatible in dry-run mode.
_PLACEHOLDER_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def _application_number() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"US-DRYRUN-{today}-{secrets.token_hex(4).upper()}"


async def submit_us_visa_dry_run(payload: USVisaApplyRequest) -> ApplyResponse:
    """Create a local US visa draft record without touching external portals."""

    app_number = _application_number()
    created_at = datetime.now(timezone.utc)
    record = {
        "application_number": app_number,
        "kind": "us_visa",
        "status": "DRAFT_CREATED",
        "user_id": payload.user_id,
        "chat_id": payload.chat_id,
        "created_at": created_at.isoformat(),
        "applicant": payload.model_dump(mode="json"),
    }
    StatusStore().upsert(app_number, record)

    return ApplyResponse(
        application_number=app_number,
        status="DRAFT_CREATED",
        user_id=payload.user_id,
        created_at=created_at,
        screenshot_base64=_PLACEHOLDER_PNG_BASE64,
        note=(
            "Dry-run record created. This scaffold does not submit DS-160 forms or automate CEAC. "
            "Use official APIs or human-in-the-loop processing only."
        ),
    )
