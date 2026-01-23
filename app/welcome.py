import telegram


async def handle_new_members(bot: telegram.Bot, message: dict) -> None:
    new_members = message["new_chat_members"]
    
    for member in new_members:
        if member.get("is_bot"):
            continue
        
        first_name = member.get("first_name", "Friend")
        welcome_msg = (
            f"Welcome to the group, {first_name}! 🎉⛷️\n\n"
            f"We're heading to Saalbach Hinterglemm! Type /help to see what I can do."
        )
        
        await bot.send_message(
            chat_id=message["chat"]["id"],
            text=welcome_msg
        )
