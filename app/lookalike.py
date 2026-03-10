import random

from app.restaurant import FREEDAY_TEAM

# Current lookalike target per chat: chat_id -> target name
_targets: dict[int, str] = {}

REACTION_EMOJIS = [
    "😱",  # scream
    "🤔",  # thinking_face
    "👀",  # eyes
    "😭",  # sob
    "🫢",  # face_with_open_eyes_and_hand_over_mouth
    "👏",  # clap
    "💀",  # skull
    "🫣",  # face_with_peeking_eye
    "🤯",  # exploding_head
]


def start_lookalike(chat_id: int) -> str:
    target = random.choice(FREEDAY_TEAM)
    _targets[chat_id] = target
    return (
        f"📸 Look-a-like challenge! Find the twin of *{target}*! "
        f"Post your photo + \"Is that you @{target}\" in the chat ⛷️!"
    )


def get_current_target(chat_id: int) -> str | None:
    return _targets.get(chat_id)


def get_random_reaction_emoji() -> str:
    return random.choice(REACTION_EMOJIS)


def message_is_lookalike_submission(message: dict) -> bool:
    chat_id = message.get("chat", {}).get("id")
    if chat_id is None:
        return False
    target = _targets.get(chat_id)
    if not target:
        return False
    has_photo = bool(message.get("photo"))
    text = (message.get("caption") or "").lower()
    mentions_target = target.lower() in text
    return has_photo and mentions_target
