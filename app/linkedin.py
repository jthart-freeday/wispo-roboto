import httpx

from app.secrets import get_secret

LINKEDIN_API_BASE = "https://api.linkedin.com/v2"
FALLBACK_MESSAGE = "Sorry, kon de LinkedIn data niet ophalen. Probeer het later nog eens!"
NO_TOKEN_MESSAGE = (
    "LinkedIn is nog niet geconfigureerd. "
    "Stel een LINKEDIN_ACCESS_TOKEN in via de environment variables of GCP Secret Manager."
)


def _get_access_token() -> str | None:
    try:
        return get_secret("linkedin-access-token")
    except (ValueError, Exception):
        return None


def _get_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "LinkedIn-Version": "202402",
    }


async def get_linkedin_profile_id(token: str) -> str | None:
    """Fetch the authenticated user's LinkedIn person URN."""
    url = f"{LINKEDIN_API_BASE}/userinfo"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, headers=_get_headers(token))
            if response.status_code != 200:
                return None
            data = response.json()
            return data.get("sub")
    except Exception:
        return None


async def get_recent_posts(token: str, person_id: str, count: int = 5) -> list[dict] | None:
    """Fetch recent posts for a LinkedIn member."""
    url = f"{LINKEDIN_API_BASE}/ugcPosts"
    params = {
        "q": "authors",
        "authors": f"List(urn:li:person:{person_id})",
        "sortBy": "LAST_MODIFIED",
        "count": count,
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, headers=_get_headers(token), params=params)
            if response.status_code != 200:
                return None
            data = response.json()
            return data.get("elements", [])
    except Exception:
        return None


async def get_post_statistics(token: str, post_urns: list[str]) -> dict[str, dict] | None:
    """Fetch engagement statistics for a list of post URNs."""
    if not post_urns:
        return {}

    url = f"{LINKEDIN_API_BASE}/organizationalEntityShareStatistics"
    shares_param = ",".join(post_urns)
    params = {
        "q": "organizationalEntity",
        "shares": f"List({shares_param})",
    }

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, headers=_get_headers(token), params=params)
            if response.status_code == 200:
                data = response.json()
                stats = {}
                for element in data.get("elements", []):
                    share = element.get("share")
                    total = element.get("totalShareStatistics", {})
                    stats[share] = total
                return stats
    except Exception:
        pass

    # Fallback: try share statistics (for personal posts)
    url = f"{LINKEDIN_API_BASE}/shareStatistics"
    params = {
        "q": "shares",
        "shares": f"List({shares_param})",
    }
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, headers=_get_headers(token), params=params)
            if response.status_code != 200:
                return None
            data = response.json()
            stats = {}
            for element in data.get("elements", []):
                share = element.get("share")
                total = element.get("totalShareStatistics", {})
                stats[share] = total
            return stats
    except Exception:
        return None


def _extract_post_text(post: dict) -> str:
    """Extract the text content from a UGC post."""
    try:
        specific_content = post.get("specificContent", {})
        share_content = specific_content.get("com.linkedin.ugc.ShareContent", {})
        share_commentary = share_content.get("shareCommentary", {})
        text = share_commentary.get("text", "")
        if text and len(text) > 80:
            return text[:77] + "..."
        return text or "(geen tekst)"
    except Exception:
        return "(geen tekst)"


def format_post_stats(posts: list[dict], stats: dict[str, dict] | None) -> str:
    """Format posts and their statistics into a readable Telegram message."""
    if not posts:
        return "Geen recente posts gevonden op LinkedIn."

    lines = ["*LinkedIn Post Statistieken*\n"]

    for i, post in enumerate(posts, 1):
        post_urn = post.get("id", "")
        text = _extract_post_text(post)
        lines.append(f"*{i}.* {text}")

        if stats and post_urn in stats:
            s = stats[post_urn]
            impressions = s.get("impressionCount", 0)
            likes = s.get("likeCount", 0)
            comments = s.get("commentCount", 0)
            shares = s.get("shareCount", 0)
            clicks = s.get("clickCount", 0)
            engagement = s.get("engagement", 0)

            lines.append(
                f"   Views: {impressions} | Likes: {likes} | "
                f"Comments: {comments} | Shares: {shares} | Clicks: {clicks}"
            )
            if engagement:
                lines.append(f"   Engagement rate: {engagement:.2%}")
        else:
            lines.append("   (statistieken niet beschikbaar)")

        lines.append("")

    return "\n".join(lines)


async def get_linkedin_post_overview() -> str:
    """Main function: fetch recent LinkedIn posts with their statistics."""
    token = _get_access_token()
    if not token:
        return NO_TOKEN_MESSAGE

    person_id = await get_linkedin_profile_id(token)
    if not person_id:
        return FALLBACK_MESSAGE + "\n(Kon profiel niet ophalen - controleer of je access token geldig is)"

    posts = await get_recent_posts(token, person_id)
    if posts is None:
        return FALLBACK_MESSAGE + "\n(Kon posts niet ophalen)"

    if not posts:
        return "Geen recente posts gevonden op je LinkedIn profiel."

    post_urns = [p.get("id", "") for p in posts if p.get("id")]
    stats = await get_post_statistics(token, post_urns)

    return format_post_stats(posts, stats)
