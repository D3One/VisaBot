"""Compatibility script kept for the repository structure from the PDF brief.

This script intentionally does not automate CEAC/DS-160, log into external visa
systems, bypass CAPTCHA, rotate proxies, or submit live applications.

Run it to generate a local dry-run application through the service layer:

    python scripts/us_visa_playwright.py sample_us_payload.json
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.models import USVisaApplyRequest
from app.services.us_visa_service import submit_us_visa_dry_run


async def main(path: str) -> None:
    payload = USVisaApplyRequest.model_validate_json(Path(path).read_text(encoding="utf-8"))
    result = await submit_us_visa_dry_run(payload)
    print(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/us_visa_playwright.py sample_us_payload.json", file=sys.stderr)
        raise SystemExit(2)
    asyncio.run(main(sys.argv[1]))
