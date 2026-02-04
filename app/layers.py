import random


def _build_layers_wear(
    village_temp: float,
    wind: float,
    snowfall: float,
    needs_mid: bool,
    needs_shell: bool,
    brutal_cold: bool,
) -> list[str]:
    wear = ["👕 Merino base (top + long johns)", "🧦 Ski socks (the only correct answer)"]
    if needs_mid:
        wear.append("🧥 Fleece or softshell mid")
    if needs_shell:
        wear.append("🦺 Waterproof shell jacket + pants")
    if brutal_cold:
        wear.append("🧤 Insulated gloves or mitts + hand warmers")
    elif village_temp < 0:
        wear.append("🧤 Proper ski gloves (not the €5 petrol station ones)")
    else:
        wear.append("🧤 Thin gloves or liners")
    wear.append("🧢 Beanie under helmet" if village_temp < -5 else "🧢 Beanie or headband")
    if wind >= 20 or village_temp < -8:
        wear.append("🧣 Neck gaiter / buff (face saver)")
    if snowfall >= 3 or wind >= 15:
        wear.append("🥽 Goggles (not sunglasses, you're not that person today)")
    else:
        wear.append("🥽 Goggles or sunglasses")
    return wear


def _cold_phrase(brutal_cold: bool, village_temp: float) -> str | None:
    if brutal_cold:
        return random.choice([
            "🥶 Respect the cold—your nose will fall off otherwise.",
            "❄️ So cold the snow is judging you.",
        ])
    if village_temp < -5:
        return random.choice([
            "❄️ Crisp, perfect skiing temp.",
            "⛷️ Cold enough to feel alive.",
        ])
    return None


def _wind_phrase(wind: float) -> str | None:
    if wind >= 30:
        return random.choice([
            "🌬️ Leave ego at home, it's windy.",
            "🌪️ The mountain is yeeting you.",
            "💨 Wind so strong your tears blow backwards.",
        ])
    if wind >= 20:
        return random.choice([
            "🌬️ Hair in face = layers in place.",
            "💨 It's not you, it's the wind.",
        ])
    if wind >= 15:
        return "🍃 Breezy."
    return None


def _snow_phrase(snowfall: float) -> str | None:
    if snowfall >= 10:
        return random.choice([
            "❄️ It's dumping.",
            "🌨️ Fresh pow doesn't care about your fashion.",
        ])
    if snowfall >= 3:
        return "🌨️ Some fresh stuff."
    return None


def _closing_phrase(
    needs_shell: bool,
    has_cold: bool,
    has_wind: bool,
    has_snow: bool,
) -> str:
    if has_cold and (has_wind or has_snow):
        return random.choice([
            "Layer like your life depends on it. Shell up.",
            "Don't skip the mid. Don't skip the shell.",
        ])
    if has_wind and needs_shell:
        return "Shell on. Your future self will thank you."
    if has_snow and needs_shell:
        return random.choice([
            "Shell keeps you dry and smug.",
            "Waterproof everything and go make some turns.",
        ])
    if needs_shell:
        return "You're not a hero, you're prepared. Layer and enjoy."
    if not (has_cold or has_wind or has_snow):
        return random.choice([
            "☀️ Don't overdo the layers or you'll be stripping in the lift queue.",
            "🌤️ A base and a shell in the bag is enough. Live a little.",
        ])
    return "Dress right and enjoy."


def _get_layers_punchline(
    village_temp: float,
    wind: float,
    snowfall: float,
    needs_shell: bool,
    brutal_cold: bool,
) -> str:
    cold = _cold_phrase(brutal_cold, village_temp)
    wind_p = _wind_phrase(wind)
    snow = _snow_phrase(snowfall)
    parts = [p for p in (cold, wind_p, snow) if p]
    closing = _closing_phrase(needs_shell, cold is not None, wind_p is not None, snow is not None)
    if not parts:
        return closing
    return " ".join(parts) + ". " + closing


def get_layers_advice(village_data: dict, mountain_data: dict) -> str:
    village_temp = village_data["current"]["temperature_2m"]
    wind = mountain_data["current"].get("wind_speed_10m") or 0
    snowfall = max(
        village_data["daily"].get("snowfall_sum", [0])[0] or 0,
        mountain_data["daily"].get("snowfall_sum", [0])[0] or 0,
    )
    needs_mid = village_temp < 0
    needs_shell = wind >= 15 or snowfall >= 2
    brutal_cold = village_temp < -12
    parts = ["Base"]
    if needs_mid:
        parts.append("mid")
    if needs_shell:
        parts.append("shell")
    layers = " + ".join(parts)
    wear = _build_layers_wear(village_temp, wind, snowfall, needs_mid, needs_shell, brutal_cold)
    punchline = _get_layers_punchline(village_temp, wind, snowfall, needs_shell, brutal_cold)
    wear_list = "\n".join(f"• {w}" for w in wear)
    return f"🧤 *Layers advice:* {layers}\n\n👔 *Wear today:*\n{wear_list}\n\n_{punchline}_"
