import asyncio
import os

import telegram

from app.shotcaller import get_shotcaller_message


async def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN")
    chat_id = int(os.environ.get("TELEGRAM_CHAT_ID", "402877939"))

    message_no_mentions = {
        "text": "/shotcaller",
        "entities": [],
        "chat": {"id": chat_id},
    }
    text = get_shotcaller_message(message_no_mentions)
    bot = telegram.Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
    print("Sent:", text[:60] + "..." if len(text) > 60 else text)


if __name__ == "__main__":
    asyncio.run(main())
