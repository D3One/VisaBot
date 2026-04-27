"""Compatibility script kept for the repository structure from the PDF brief.

This script intentionally does not automate VFS/Schengen portals, log into
external systems, solve hCaptcha, call Browserless unblock endpoints, rotate
proxies, or submit live applications.

Run it to generate a local dry-run application through the service layer:

    python scripts/schengen_playwright.py sample_schengen_payload.json
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.models import SchengenApplyRequest
from app.services.schengen_service import submit_schengen_dry_run


async def main(path: str) -> None:
    payload = SchengenApplyRequest.model_validate_json(Path(path).read_text(encoding="utf-8"))
    result = await submit_schengen_dry_run(payload)
    print(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/schengen_playwright.py sample_schengen_payload.json", file=sys.stderr)
        raise SystemExit(2)
    asyncio.run(main(sys.argv[1]))
