import logging
import random

BASE_URL_FULL = "https://images.webcamgalore.com/{id}-current-webcam-{location}.jpg"

SAALBACH_WEBCAMS: list[tuple[str, str, str]] = [
    ("037194", "PANOMAX Reiterkogel", "Saalbach-Hinterglemm"),
    ("022162", "360° View of Hinterglemm", "Hinterglemm"),
    ("027437", "View onto Hinterglemm", "Hinterglemm"),
    ("029619", "Panorama Saalbach Center", "Saalbach"),
    ("028248", "PANOMAX Zwölferkogel (1984 m)", "Hinterglemm"),
    ("034925", "PANOMAX Maisalm Saalbach", "Saalbach"),
]

_log = logging.getLogger(__name__)


def get_saalbach_webcam_url() -> tuple[str, str]:
    cam_id, cam_name, location = random.choice(SAALBACH_WEBCAMS)
    url = BASE_URL_FULL.format(id=int(cam_id), location=location)
    _log.info("mountainview: selected cam %s (%s) url=%s", cam_id, cam_name, url)
    return url, cam_name
