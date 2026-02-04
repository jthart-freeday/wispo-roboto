import random


def _user_to_dict(user: dict | object) -> dict | None:
    if user is None:
        return None
    if isinstance(user, dict):
        uid = user.get("id")
        if uid is None:
            return None
        return {
            "id": uid,
            "first_name": user.get("first_name") or "",
            "username": user.get("username") or "",
        }
    uid = getattr(user, "id", None)
    if uid is None:
        return None
    if getattr(user, "is_bot", False):
        return None
    return {
        "id": uid,
        "first_name": getattr(user, "first_name", "") or "",
        "username": getattr(user, "username", "") or "",
    }


def _add_text_mention_entity(ent: dict, seen_ids: set[int], result: list[dict]) -> None:
    u = ent.get("user")
    if not u or not isinstance(u, dict) or not u.get("id") or u.get("is_bot"):
        return
    entry = _user_to_dict(u)
    if entry and entry["id"] not in seen_ids:
        seen_ids.add(entry["id"])
        result.append(entry)


def _mentioned_users(message: dict) -> list[dict]:
    entities = message.get("entities") or []
    seen_ids: set[int] = set()
    result: list[dict] = []
    for ent in entities:
        if not isinstance(ent, dict):
            continue
        if ent.get("type") == "text_mention":
            _add_text_mention_entity(ent, seen_ids, result)
    return [r for r in result if r]


def get_shotcaller_message(message: dict) -> str:
    mentioned = _mentioned_users(message)
    from_data = message.get("from")
    if isinstance(from_data, dict) and from_data.get("is_bot"):
        from_data = None
    sender_entry = _user_to_dict(from_data)
    seen = set()
    candidates: list[dict] = []
    if sender_entry and sender_entry["id"] not in seen:
        seen.add(sender_entry["id"])
        candidates.append(sender_entry)
    for m in mentioned:
        if m["id"] not in seen:
            seen.add(m["id"])
            candidates.append(m)
    if not candidates:
        return "Mention someone! Usage: /shotcaller @user1 @user2"
    chosen = random.choice(candidates)
    user_id = chosen["id"]
    first_name = chosen["first_name"] or chosen["username"] or "Someone"
    mention = f"[{first_name}](tg://user?id={user_id})"
    lines = [
        f"Shotcaller says: {mention} — you're up! 🥃 Take a shot!",
        f"The bottle has spoken. {mention}, your soul is required. 🥃",
        f"🎲 Rolled the dice. {mention} — drink. No backsies. 🥃",
        f"Everybody point at {mention}. They're taking one for the team. 🥃",
        f"Plot twist: {mention} has been selected. The shot chooses the drinker. 🥃",
        f"Not it! Oh wait — {mention}, you're it. 🥃",
        f"Attention please: {mention} is legally required to take a shot. (We made it up. Do it anyway.) 🥃",
        f"🥃 {mention} — the universe has aligned. Your shot awaits.",
        f"Hot take: {mention} should definitely have a shot right now. 🥃",
        f"Breaking news: {mention} has been chosen. Shot o'clock. 🥃",
        f"Sorry {mention}, the council has decided. One shot. No appeal. 🥃",
        f"Shots! Shots! Shots! … and {mention} is up first. 🥃",
    ]
    return random.choice(lines)
