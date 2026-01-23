import httpx


async def get_saalbach_webcam_image() -> bytes | None:
    webcam_url = "https://images.webcamgalore.com/webcamimages/webcam-037194.jpg"
    
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get(webcam_url)
            if response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"):
                return response.content
            return None
    except Exception:
        return None
