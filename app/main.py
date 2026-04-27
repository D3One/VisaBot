from fastapi import FastAPI

from app.core.config import get_settings
from app.routers import schengen, us_visa

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "Safe FastAPI scaffold for visa assistant workflows. "
        "Dry-run only: no live portal automation, CAPTCHA bypass, or anti-bot evasion."
    ),
)

app.include_router(us_visa.router)
app.include_router(schengen.router)


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}
