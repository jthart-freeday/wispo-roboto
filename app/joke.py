import httpx


async def get_joke() -> str:
    url = "https://api.jokes.one/jod"

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            
            if response.status_code != 200:
                return "Sorry, couldn't fetch a joke right now. The joke's on me! 😅"
            
            data = response.json()
            title = data["contents"]["jokes"][0]["joke"]["title"]
            text = data["contents"]["jokes"][0]["joke"]["text"]
            return f"{title}\n\n{text}\n🤣🤣🤣"
    except Exception:
        return "Sorry, couldn't fetch a joke right now. The joke's on me! 😅"
