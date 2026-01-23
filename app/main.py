from typing import Any

import telegram
from fastapi import FastAPI, Response

from app.array_extensions import key_exists
from app.commands import handle_command
from app.forecast import send_daily_forecast
from app.secrets import get_telegram_api_key
from app.welcome import handle_new_members

app = FastAPI()

JSON_MEDIA_TYPE = "application/json"


@app.post("/message")
async def message_stuff(request_data: dict[str, Any]) -> Response:
    print(request_data)
    message = get_message_or_update(request_data)

    if not message:
        return Response(status_code=202, media_type=JSON_MEDIA_TYPE)

    bot = telegram.Bot(token=get_telegram_api_key())

    if key_exists(message, "new_chat_members"):
        await handle_new_members(bot, message)
        return Response(status_code=202, media_type=JSON_MEDIA_TYPE)

    if not key_exists(message, "text") or not message["text"].startswith("/"):
        return Response(status_code=202, media_type=JSON_MEDIA_TYPE)

    await handle_command(bot, message)

    return Response(status_code=202, media_type=JSON_MEDIA_TYPE)


def get_message_or_update(update: dict) -> dict | None:
    if key_exists(update, "edited_message"):
        return update["edited_message"]
    if key_exists(update, "message"):
        return update["message"]
    return None


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/forecast")
async def trigger_forecast() -> dict[str, str]:
    await send_daily_forecast()
    return {"status": "forecast sent"}
