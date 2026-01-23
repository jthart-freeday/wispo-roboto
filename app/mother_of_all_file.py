import random
import re

names = ["Amy", "Yoni", "Rutger", "Irene", "Tijs"]


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


def get_name() -> str:
    return random.choice(names)


def get_manly() -> str:
    nmb = random.randint(1, 30)
    return "8" + nmb * "=" + "D"


def get_flip() -> str:
    return "(╯°□°)╯︵ ┻━┻"


def get_back() -> str:
    return "┬─┬ノ( º _ ºノ)"


def get_address() -> str:
    return "Adler Resort, Hasenbachweg 378, 5753 Saalbach, Oostenrijk"


def get_addresshotel() -> str:
    return "Adler Resort, Hasenbachweg 378, 5753 Saalbach, Oostenrijk"


def get_mansplain() -> str:
    return """
    Milena is a software engineer.
    She’s reviewing a pull request and says:

    “We shouldn’t do it this way, it’ll break when the async job retries.”

    A male colleague leans back in his chair.

    “Yeah, so the thing with async jobs,” he says, “is that they can retry.”

    Milena pauses.

    “Yes,” she replies. “That’s what I just said.”

    He continues anyway.

    He explains what async means.
    He explains what retries are.
    He explains why retries might be dangerous.

    He concludes with confidence:

    “So yeah, we should be careful here.”

    Milena nods.

    They change the code exactly the way she suggested —
    but now it’s his idea.

    That’s mansplaining.
    ![mansplain](https://i.imgur.com/5seN7JL.png)
    """


