import json
import os
from pathlib import Path
from threading import Lock
from typing import Any

from app.core.config import get_settings
from app.models import utc_now


_LOCK = Lock()


class StatusStore:
    """Tiny JSON-file store for local/demo deployments.

    Replace with PostgreSQL, MongoDB, DynamoDB, etc. for production.
    """

    def __init__(self, path: str | None = None) -> None:
        settings = get_settings()
        self.path = Path(path or settings.storage_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}
        with self.path.open("r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}

    def _write(self, data: dict[str, Any]) -> None:
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        with tmp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
        os.replace(tmp_path, self.path)

    def upsert(self, application_number: str, record: dict[str, Any]) -> dict[str, Any]:
        with _LOCK:
            data = self._read()
            now = utc_now().isoformat()
            existing = data.get(application_number, {})
            merged = {**existing, **record, "updated_at": now}
            data[application_number] = merged
            self._write(data)
            return merged

    def get(self, application_number: str) -> dict[str, Any] | None:
        with _LOCK:
            data = self._read()
            return data.get(application_number)
