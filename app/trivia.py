import html
import random
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

QUESTION_EXPIRY_MINUTES = 5
RATE_LIMIT_QUESTIONS = 5
RATE_LIMIT_HOURS = 1

API_URL = "https://opentdb.com/api.php?amount=1&type=multiple"

LETTERS = ["A", "B", "C", "D"]


@dataclass
class TriviaQuestion:
    user_id: int
    user_name: str
    correct_answer: str
    timestamp: datetime


@dataclass
class TriviaScore:
    user_name: str
    correct: int
    total: int


_active_questions: dict[int, TriviaQuestion] = {}
_scores: dict[int, TriviaScore] = {}
_user_requests: dict[int, list[datetime]] = {}


def _cleanup_expired_questions() -> None:
    now = datetime.now(timezone.utc)
    expired = [
        mid
        for mid, q in _active_questions.items()
        if (now - q.timestamp).total_seconds() > QUESTION_EXPIRY_MINUTES * 60
    ]
    for mid in expired:
        del _active_questions[mid]


def _is_rate_limited(user_id: int) -> bool:
    now = datetime.now(timezone.utc)
    if user_id in _user_requests:
        _user_requests[user_id] = [
            ts
            for ts in _user_requests[user_id]
            if (now - ts).total_seconds() < RATE_LIMIT_HOURS * 3600
        ]
    else:
        _user_requests[user_id] = []
    return len(_user_requests[user_id]) >= RATE_LIMIT_QUESTIONS


RATE_LIMITED = "rate_limited"
API_ERROR = "api_error"


async def get_trivia_question(
    user_id: int, user_name: str
) -> tuple[str, str] | str:
    """Returns (message_text, correct_letter) or an error string."""
    _cleanup_expired_questions()

    if _is_rate_limited(user_id):
        return RATE_LIMITED

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(API_URL, timeout=10)
            resp.raise_for_status()
            data = resp.json()
    except (httpx.HTTPError, Exception):
        return API_ERROR

    if data.get("response_code") != 0 or not data.get("results"):
        return API_ERROR

    result = data["results"][0]
    category = html.unescape(result["category"])
    question_text = html.unescape(result["question"])
    correct = html.unescape(result["correct_answer"])
    incorrect = [html.unescape(a) for a in result["incorrect_answers"]]

    options = [correct] + incorrect
    random.shuffle(options)
    correct_letter = LETTERS[options.index(correct)]

    _user_requests.setdefault(user_id, []).append(datetime.now(timezone.utc))

    lines = [
        f"🧠 *Trivia for {user_name}!*",
        "",
        f"Category: {category}",
        f"{question_text}",
        "",
    ]
    for i, option in enumerate(options):
        lines.append(f"{LETTERS[i]}) {option}")
    lines.append("")
    lines.append("Reply to this message with your answer (A, B, C, or D)")

    return "\n".join(lines), correct_letter


def store_question(
    bot_message_id: int, user_id: int, user_name: str, correct_answer: str
) -> None:
    _active_questions[bot_message_id] = TriviaQuestion(
        user_id=user_id,
        user_name=user_name,
        correct_answer=correct_answer,
        timestamp=datetime.now(timezone.utc),
    )


def handle_trivia_reply(message: dict) -> str | None:
    reply_to = message.get("reply_to_message")
    if not reply_to:
        return None

    bot_msg_id = reply_to.get("message_id")
    if bot_msg_id not in _active_questions:
        return None

    question = _active_questions[bot_msg_id]
    user_id = message["from"]["id"]

    if user_id != question.user_id:
        return "This trivia question isn't for you! Use /trivia to get your own question."

    answer = message.get("text", "").strip().upper()
    if answer not in LETTERS:
        return "Please reply with A, B, C, or D."

    del _active_questions[bot_msg_id]

    user_name = question.user_name
    if user_id not in _scores:
        _scores[user_id] = TriviaScore(user_name=user_name, correct=0, total=0)

    score = _scores[user_id]
    score.total += 1
    score.user_name = user_name

    if answer == question.correct_answer:
        score.correct += 1
        return f"✅ Correct! Nice one, {user_name}! Your score: {score.correct}/{score.total}"
    else:
        return f"❌ Wrong! The answer was {question.correct_answer}. Your score: {score.correct}/{score.total}"


def get_leaderboard() -> str:
    if not _scores:
        return "No trivia scores yet. Be the first! /trivia"

    sorted_scores = sorted(_scores.values(), key=lambda s: s.correct, reverse=True)
    lines = ["🏆 *Trivia Leaderboard*\n"]
    for i, s in enumerate(sorted_scores, 1):
        lines.append(f"{i}. {s.user_name} — {s.correct}/{s.total} correct")

    return "\n".join(lines)
