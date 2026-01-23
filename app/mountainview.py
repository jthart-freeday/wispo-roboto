import random

import httpx


async def get_saalbach_webcam_image() -> bytes | None:
    webcam_urls = [
        "https://cams.snow-online.de/images/ecu/content/c_webcam/kohlmais--saalbach-hinterglemm_n473584-70768-0_raw.jpg",
        "https://images.webcamgalore.com/webcamimages/webcam-037194.jpg",
    ]
    
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            for url in webcam_urls:
                try:
                    response = await client.get(url)
                    if response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"):
                        return response.content
                except Exception:
                    continue
            
            return None
    except Exception:
        return None
