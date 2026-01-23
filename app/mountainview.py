import random

import httpx


async def get_saalbach_webcam_image() -> str | None:
    webcam_urls = [
        "https://cams.skigebiete-test.de/images/ecu/content/c_webcam/kohlmais--saalbach-hinterglemm_n473584-70768-0_raw.jpg",
        "https://images.webcamgalore.com/webcamimages/webcam-037194.jpg",
    ]
    
    try:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            for url in webcam_urls:
                try:
                    response = await client.head(url)
                    if response.status_code == 200:
                        return url
                except Exception:
                    continue
            
            return random.choice(webcam_urls)
    except Exception:
        return random.choice(webcam_urls)
