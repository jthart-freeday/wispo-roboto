import httpx

FALLBACK_MESSAGE = "Sorry, couldn't fetch a joke right now. The joke's on me! 😅"


async def get_joke() -> str:
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            
            if response.status_code != 200:
                return FALLBACK_MESSAGE
            
            data = response.json()
            
            if data.get("error"):
                return FALLBACK_MESSAGE
            
            if data.get("type") == "single":
                return f"{data['joke']}\n\n🤣"
            else:
                return f"{data['setup']}\n\n{data['delivery']}\n\n🤣"
    except Exception:
        return FALLBACK_MESSAGE
