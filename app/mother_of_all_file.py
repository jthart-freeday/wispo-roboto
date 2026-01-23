import random
import re

names = ["Mark Jan"]


def get_rng(message_text: str) -> str:
    if message_text == "rng":
        output = "please use this function as follows: rng{number}, for the random number generator"
    elif "rng" in message_text:
        try:
            new = re.findall(r"rng(\w+)", message_text)[0]
            components = re.split(r"(\d+)", new)
            output = "The magic number is : " + str(
                random.randint(1, [int(word) for word in components if word.isdigit()][0])
            )
        except Exception:
            output = "You are probably doing something wrong, you fool. Format: rng{number}"
    else:
        output = "yeeez, just use it the way you are supposed to, idiot. Format: rng{number}"
    return output


def get_name(message: dict) -> str:
    if "from" not in message:
        return random.choice(names)
    
    user = message["from"]
    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")
    username = user.get("username", "")
    
    if first_name and last_name:
        return f"{first_name} {last_name}"
    elif first_name:
        return first_name
    elif username:
        return username
    return random.choice(names)


def get_flip() -> str:
    return "(╯°□°)╯︵ ┻━┻"


def get_back() -> str:
    return "┬─┬ノ( º _ ºノ)"


def get_address() -> str:
    return "Adler Resort, Hasenbachweg 378, 5753 Saalbach, Oostenrijk"


def get_addresshotel() -> str:
    return "Adler Resort, Hasenbachweg 378, 5753 Saalbach, Oostenrijk"


def get_mansplain_image_url() -> str:
    return "https://cdn.freeday.ai/wintersport/Screenshot%202025-08-13%20at%2014.13.16.png"


