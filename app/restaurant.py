import random


FREEDAY_TEAM = [
    "Ties", "Joost", "Philip", "Karan", "Marcus", "MJ", "Gijs", "Emile",
    "Milena", "Marieke", "Dagmar", "Melanie", "Djovanni", "Nemanja", "Mathijs",
    "Jasmijn", "Javier", "Pieter", "Lucas", "Hella", "Bo", "Willem",
    "Jonathan", "Guust", "Konstantina",
]

MISBEHAVIORS = [
    "will definitely try to order off-menu in broken German",
    "is not allowed to touch the wine list tonight",
    "has been pre-banned from the dessert buffet",
    "will 100% complain the Schnitzel is bigger than their face",
    "is already googling 'how to split the bill 25 ways'",
    "will pretend to be a food critic on TripAdvisor",
    "is on napkin-folding duty for the entire table",
    "must sit at the kids' table after last time",
    "will try to pay with a firm handshake and a smile",
    "has been caught stealing breadsticks. Again.",
    "will attempt to order Kaiserschmarrn as a main course",
    "is responsible for the group's noise complaint",
    "will somehow end up in the kitchen 'helping' the chef",
    "is banned from making toasts longer than 10 seconds",
    "will accidentally knock over someone's beer. It's tradition.",
    "has to explain to the waiter why we need 25 separate receipts",
    "will try to convince everyone that tap water counts as a round",
    "is already asleep in the corner booth",
    "will loudly mispronounce every item on the menu",
    "got us kicked out of here last year. Let's see if they remember.",
]

RESTAURANTS = [
    # --- Fine Dining & Upscale ---
    {
        "name": "Gold & Pepper",
        "vibe": "The fanciest spot in Saalbach – local ingredients meet international cuisine",
        "type": "Fine dining",
    },
    {
        "name": "Ess:Enz",
        "vibe": "Gastronomic journey from mountains to sea, Alpine cuisine with a Mediterranean touch",
        "type": "Fine dining",
    },
    {
        "name": "Montana Royal Alpin Club",
        "vibe": "Modern mountain restaurant with eclectic vibes",
        "type": "Fine dining / Austrian",
    },
    {
        "name": "Xandl Stadl",
        "vibe": "High quality food right on the slopes with DJ sets",
        "type": "Fine dining / Austrian",
    },
    {
        "name": "Der Jennerwein",
        "vibe": "Fantastic steakhouse with exceptional service",
        "type": "Steakhouse / Grill",
    },
    {
        "name": "Altitude Grill",
        "vibe": "Modern twist on classics at Adler Resort, with sushi nights",
        "type": "Steakhouse / Grill",
    },
    # --- Mountain Huts ---
    {
        "name": "Rosswaldhütte",
        "vibe": "Top-notch mountain stopover – don't miss the Kaiserschmarrn",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Sonnalm",
        "vibe": "Incredible homemade products with impeccable service",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Walleggalm",
        "vibe": "Legendary slope-side hut at 1500m – cheese dumplings, Kaiserschmarrn & Tomahawk steak",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Maisalm",
        "vibe": "Contemporary hut blending traditional with modern, great sun terrace",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Luis Alm",
        "vibe": "Slope-side with stunning views and a casual vibe",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Thurneralm",
        "vibe": "Authentic Austrian cuisine in alpine scenery – pouring drinks since the 1800s",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Reiteralm",
        "vibe": "Rustic and cozy with top quality dishes, try the ribs or baked trout",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Wieser Alm",
        "vibe": "Modern alpine hut near the Reiterkogel lift with delicious meals",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Panorama-Alm",
        "vibe": "Fantastic mountain location with a playground for the kids",
        "type": "Mountain hut / Austrian",
    },
    {
        "name": "Winkleralm",
        "vibe": "Cozy hut at the mid-station of the Zwölferkogel",
        "type": "Mountain hut / Austrian",
    },
    # --- Après-ski & Party ---
    {
        "name": "Goaßstall",
        "vibe": "Legendary après-ski right on the slopes – cheap drinks, great music from 3pm",
        "type": "Après-ski / Fast food",
    },
    {
        "name": "Hinterhag Alm",
        "vibe": "Incredible après-ski with live music from 4 to 7pm",
        "type": "Après-ski / Austrian",
    },
    {
        "name": "Bauer's Schi-Alm",
        "vibe": "Vibrant après-ski hotspot with four distinct bars",
        "type": "Après-ski / Austrian",
    },
    {
        "name": "eva, ALM",
        "vibe": "Heart of Saalbach with live music and great cuisine",
        "type": "Après-ski / Austrian",
    },
    {
        "name": "Der Schwarzacher",
        "vibe": "Lively après-ski with a DJ and party atmosphere",
        "type": "Après-ski / Austrian",
    },
    # --- Village Restaurants ---
    {
        "name": "Schattberg Stube",
        "vibe": "Outstanding quality traditional gastronomy in the center",
        "type": "Austrian",
    },
    {
        "name": "Restaurant Heurigenstube",
        "vibe": "Delectable dishes with exceptional service at Hotel Salzburg",
        "type": "Austrian",
    },
    {
        "name": "Westernstadl",
        "vibe": "Hidden gem with Western theme and fantastic burgers",
        "type": "Burger / Austrian",
    },
    {
        "name": "Restaurant s'Wirtshaus",
        "vibe": "88-year-old establishment with a warm and inviting interior",
        "type": "Austrian",
    },
    {
        "name": "Gasthaus Eichenheim",
        "vibe": "Romantic dinner spot with fine regional cooking",
        "type": "Austrian",
    },
    {
        "name": "happYellow Restaurant",
        "vibe": "Popular for romantic dining and family-friendly meals",
        "type": "Austrian",
    },
    {
        "name": "Liemers",
        "vibe": "Solid restaurant in Hinterglemm at Hotel Reiterkogel",
        "type": "Austrian",
    },
    {
        "name": "Thomsn",
        "vibe": "Well-regarded spot in Hinterglemm near Hotel Salzburg",
        "type": "Austrian",
    },
    {
        "name": "Seppi's Restaurant",
        "vibe": "Cozy Italian vibes in the village",
        "type": "Italian",
    },
    {
        "name": "Soul House",
        "vibe": "International flair with Austrian roots",
        "type": "International / Austrian",
    },
    {
        "name": "Bauer's Mein Lokal",
        "vibe": "Casual all-day dining with Austrian comfort food",
        "type": "Austrian / Café",
    },
    {
        "name": "Das K by Tobi",
        "vibe": "Quick bites and drinks with Austrian flair",
        "type": "Austrian / Bar",
    },
    {
        "name": "Hotel Astrid",
        "vibe": "Classic Austrian hotel restaurant",
        "type": "Austrian",
    },
    {
        "name": "mitterer",
        "vibe": "Local Austrian cuisine done right",
        "type": "Austrian",
    },
    # --- Italian / Pizza ---
    {
        "name": "Mangia! Pizzeria Napoletana",
        "vibe": "The most authentic Italian restaurant in the area",
        "type": "Italian / Pizza",
    },
    {
        "name": "Del Rossi",
        "vibe": "Charming restaurant with modern decor and gluten-free options",
        "type": "Italian / Austrian",
    },
    {
        "name": "Bar Napoli",
        "vibe": "Popular pizzeria with flavors that burst",
        "type": "Pizza",
    },
    {
        "name": "La Trattoria",
        "vibe": "Mediterranean and Italian classics",
        "type": "Italian / Mediterranean",
    },
]


def get_random_restaurant() -> str:
    pick = random.choice(RESTAURANTS)
    troublemaker = random.choice(FREEDAY_TEAM)
    misbehavior = random.choice(MISBEHAVIORS)
    return (
        f"🍽️ *Tonight's pick:* {pick['name']}\n"
        f"🏷️ {pick['type']}\n"
        f"💬 {pick['vibe']}\n\n"
        f"⚠️ *Heads up:* {troublemaker} {misbehavior}\n\n"
        f"Guten Appetit! 🇦🇹"
    )
