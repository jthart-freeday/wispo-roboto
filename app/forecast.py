import logging
import random
import re
from datetime import date

import httpx
import telegram
from bs4 import BeautifulSoup

from app.secrets import get_telegram_api_key

SAALBACH_WEATHER_URL = "https://www.saalbach.com/en/live-info/weather/weather-for-external-websites"

TELEGRAM_CHAT_ID = -5036926629
SAALBACH_LAT = 47.3917
SAALBACH_LON = 12.6364

# Elevations in meters
VILLAGE_ELEVATION = 1003  # Saalbach village
MOUNTAIN_ELEVATION = 2096  # Schattberg summit


def get_snow_depth_comment(depth_cm: float) -> str:
    if depth_cm >= 150:
        return "DEEP POWDER PARADISE! 🤩"
    elif depth_cm >= 100:
        return "Waist-deep powder! 😍"
    elif depth_cm >= 50:
        return "Knee-deep! Perfect! 🎿"
    elif depth_cm >= 20:
        return "Not bad! 👍"
    else:
        return "Needs more snow! 🙏"


def get_fresh_snow_alert(snowfall_cm: float) -> str:
    if snowfall_cm >= 20:
        return "🚨 MASSIVE POWDER ALERT! IT'S DUMPING! 🚨"
    elif snowfall_cm >= 10:
        return "🎉 POWDER ALERT! Fresh pow incoming! 🎉"
    elif snowfall_cm >= 5:
        return "❄️ Nice! Some fresh snow! ❄️"
    return ""


def get_temp_comment(temp: float) -> str:
    if temp < -15:
        return "🥶 BRUTALLY COLD! Layer up!"
    elif temp < -10:
        return "🥶 Freezing! Bundle up!"
    elif temp < -5:
        return "❄️ Cold and crisp!"
    elif temp < 0:
        return "Perfect skiing temp!"
    elif temp < 5:
        return "☀️ Spring skiing weather!"
    else:
        return "🌡️ Getting warm! Morning runs recommended!"


def get_condition_rating(mountain_snow: float, snowfall: float, temp: float) -> str:
    score = 0
    
    if mountain_snow >= 100:
        score += 2
    elif mountain_snow >= 50:
        score += 1
    
    if snowfall >= 10:
        score += 2
    elif snowfall >= 5:
        score += 1
    
    if -10 <= temp <= 0:
        score += 1
    
    if score >= 5:
        return "⭐⭐⭐⭐⭐ EPIC CONDITIONS!"
    elif score >= 3:
        return "⭐⭐⭐⭐ Excellent skiing!"
    elif score >= 2:
        return "⭐⭐⭐ Good conditions!"
    else:
        return "⭐⭐ We'll make it work! 💪"


def get_countdown_message(days: int) -> str:
    if days <= 0:
        return "🎉 IT'S HERE! IT'S HAPPENING! LET'S GOOOOO! 🎉"
    elif days == 1:
        return "🔥 TOMORROW!!! ONE MORE SLEEP!! 🔥"
    elif days <= 3:
        return f"🚨 {days} DAYS! PACKING TIME! 🎒"
    elif days <= 7:
        return f"⏰ {days} days! Almost time to shred! 🏂"
    elif days <= 14:
        return f"📅 {days} days! Next week(ish)! Getting close! 🎿"
    else:
        messages = [
            f"⏳ {days} days! Time to start doing squats! 🏋️",
            f"🗓️ {days} days! Have you waxed your skis yet? 🎿",
            f"⛷️ {days} days until SHRED TIME! 🤘",
            f"🏔️ {days} days! The mountains are calling! 📞",
            f"❄️ {days} days! Start planning your après! 🍻",
            f"🎿 {days} days! Time flies when you're excited! ⏰",
        ]
        return random.choice(messages)


def make_forecast(village: dict, mountain: dict) -> str:
    village_temp = village["current"]["temperature_2m"]
    village_snow_m = village["current"].get("snow_depth", 0) or 0
    village_snow = village_snow_m * 100
    village_snowfall = village["daily"]["snowfall_sum"][0] or 0
    
    mountain_temp = mountain["current"]["temperature_2m"]
    mountain_snow_m = mountain["current"].get("snow_depth", 0) or 0
    mountain_snow = mountain_snow_m * 100
    mountain_snowfall = mountain["daily"]["snowfall_sum"][0] or 0
    
    days = (date(2026, 3, 11) - date.today()).days
    
    max_snowfall = max(village_snowfall, mountain_snowfall)
    fresh_snow_alert = get_fresh_snow_alert(max_snowfall)
    condition_rating = get_condition_rating(mountain_snow, mountain_snowfall, mountain_temp)
    countdown = get_countdown_message(days)
    
    msg = "Hi there! ⛷🏂\n\n"
    
    if fresh_snow_alert:
        msg += f"{fresh_snow_alert}\n\n"
    
    msg += f"*{condition_rating}*\n\n"
    
    msg += "📊 *Weather Update for Saalbach Hinterglemm:*\n\n"
    
    msg += f"🏘️ *Village* ({VILLAGE_ELEVATION}m)\n"
    msg += f"  • Temperature: {village_temp}°C {get_temp_comment(village_temp)}\n"
    msg += f"  • Snow depth: {village_snow:.0f}cm\n"
    msg += f"  • Fresh snow: {village_snowfall:.1f}cm\n\n"
    
    msg += f"🏔️ *Mountain* ({MOUNTAIN_ELEVATION}m)\n"
    msg += f"  • Temperature: {mountain_temp}°C {get_temp_comment(mountain_temp)}\n"
    msg += f"  • Snow depth: {mountain_snow:.0f}cm - {get_snow_depth_comment(mountain_snow)}\n"
    msg += f"  • Fresh snow: {mountain_snowfall:.1f}cm\n\n"
    
    msg += f"*{countdown}*"
    
    return msg


def _parse_saalbach_weather(html: str) -> tuple[dict, dict] | None:
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        if "Valley" in table.get_text() and "Top" in table.get_text():
            break
    else:
        return None
    tds = table.find_all("td")
    temps = []
    snows = []
    for td in tds:
        content = td.get_text(strip=True)
        temp_match = re.match(r"(-?\d+)\s*°", content)
        if temp_match:
            temps.append(int(temp_match.group(1)))
        snow_match = re.match(r"(\d+)\s*cm", content)
        if snow_match:
            snows.append(int(snow_match.group(1)))
    if len(temps) < 3 or len(snows) < 3:
        return None
    valley_temp, mid_temp, top_temp = temps[0], temps[1], temps[2]
    valley_snow, mid_snow, top_snow = snows[0], snows[1], snows[2]
    village = {
        "current": {"temperature_2m": valley_temp, "snow_depth": valley_snow / 100},
        "daily": {"snowfall_sum": [0]},
    }
    mountain = {
        "current": {"temperature_2m": top_temp, "snow_depth": top_snow / 100},
        "daily": {"snowfall_sum": [0]},
    }
    return village, mountain


async def get_saalbach_snow_report() -> tuple[dict, dict] | None:
    try:
        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True,
            headers={"User-Agent": "WispoRoboto/1.0 (Saalbach snow report)"},
        ) as client:
            resp = await client.get(SAALBACH_WEATHER_URL)
            if resp.status_code != 200:
                return None
            result = _parse_saalbach_weather(resp.text)
            if result:
                logging.info("Saalbach official weather parsed successfully")
            return result
    except Exception as e:
        logging.warning("Saalbach snow report fetch failed: %s", e)
        return None


async def get_weather_data(elevation: int, include_wind: bool = False) -> dict:
    current = ["temperature_2m", "snow_depth"]
    if include_wind:
        current.extend(["wind_speed_10m"])
    params = {
        "latitude": SAALBACH_LAT,
        "longitude": SAALBACH_LON,
        "elevation": elevation,
        "current": current,
        "daily": ["snowfall_sum", "temperature_2m_max", "temperature_2m_min"],
        "timezone": "Europe/Berlin",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
        logging.info(f"Weather API response ({elevation}m): {resp.status_code}")
        return resp.json()


async def send_message(bot: telegram.Bot, msg: str, chat_id: int) -> None:
    await bot.send_message(text=msg, chat_id=chat_id, parse_mode="Markdown")


async def send_daily_forecast() -> None:
    logging.info("Sending daily forecast")
    bot = telegram.Bot(token=get_telegram_api_key())

    resort_data = await get_saalbach_snow_report()
    if resort_data:
        village_data, mountain_data = resort_data
    else:
        village_data = await get_weather_data(VILLAGE_ELEVATION)
        mountain_data = await get_weather_data(MOUNTAIN_ELEVATION)
    await send_message(bot, make_forecast(village_data, mountain_data), TELEGRAM_CHAT_ID)
