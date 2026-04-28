from __future__ import annotations

import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def send_telegram_message(chat_id: int | str | None, text: str, parse_mode: str = "HTML") -> bool:
    """Send a Telegram message to the chat_id provided by the API request.

    The bot token is still loaded from environment variables, but the destination
    chat_id is no longer global configuration. This lets one running API container
    notify different Telegram chats without changing .env or restarting Docker.

    Returns True when the message was sent. Returns False when Telegram is not
    configured, chat_id is missing, or the Telegram API request fails.
    """

    settings = get_settings()
    if not settings.bot_token:
        logger.info("Telegram bot token is not configured; skipping notification.")
        return False

    if chat_id is None:
        logger.info("Telegram chat_id was not provided; skipping notification.")
        return False

    url = f"https://api.telegram.org/bot{settings.bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
        return True
    except httpx.HTTPError as exc:
        logger.warning("Telegram notification failed: %s", exc)
        return False
