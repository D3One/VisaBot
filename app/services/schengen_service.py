import base64
import secrets
from datetime import datetime, timezone

from app.models import ApplyResponse, SchengenApplyRequest
from app.services.store import StatusStore


def _application_number() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"SCH-DRYRUN-{today}-{secrets.token_hex(4).upper()}"


def _escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _minimal_pdf_bytes(title: str, body_lines: list[str]) -> bytes:
    """Generate a tiny valid PDF without extra dependencies."""

    lines = [f"BT /F1 18 Tf 72 760 Td ({_escape_pdf_text(title)}) Tj ET"]
    y = 730
    for line in body_lines[:12]:
        lines.append(f"BT /F1 11 Tf 72 {y} Td ({_escape_pdf_text(line)}) Tj ET")
        y -= 18
    stream = "\n".join(lines).encode("latin-1", errors="replace")

    objects: list[bytes] = []
    objects.append(b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj")
    objects.append(b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj")
    objects.append(
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj"
    )
    objects.append(b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj")
    objects.append(b"5 0 obj << /Length " + str(len(stream)).encode() + b" >> stream\n" + stream + b"\nendstream endobj")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj + b"\n")
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode()
    )
    return bytes(pdf)


async def submit_schengen_dry_run(payload: SchengenApplyRequest) -> ApplyResponse:
    """Create a local Schengen visa draft record without touching external portals."""

    app_number = _application_number()
    created_at = datetime.now(timezone.utc)
    record = {
        "application_number": app_number,
        "kind": "schengen",
        "status": "DRAFT_CREATED",
        "user_id": payload.user_id,
        "created_at": created_at.isoformat(),
        "applicant": payload.model_dump(mode="json"),
    }
    StatusStore().upsert(app_number, record)

    pdf = _minimal_pdf_bytes(
        "Schengen Dry-Run Draft",
        [
            f"Application number: {app_number}",
            f"Target country: {payload.target_country}",
            f"Applicant: {payload.given_name} {payload.surname}",
            f"Arrival date: {payload.arrival_date}",
            "This is a local dry-run artifact, not an official visa form.",
        ],
    )

    return ApplyResponse(
        application_number=app_number,
        status="DRAFT_CREATED",
        user_id=payload.user_id,
        created_at=created_at,
        pdf_base64=base64.b64encode(pdf).decode("ascii"),
        note=(
            "Dry-run record created. This scaffold does not submit VFS/Schengen forms, "
            "does not solve CAPTCHA, and does not bypass anti-bot controls."
        ),
    )
