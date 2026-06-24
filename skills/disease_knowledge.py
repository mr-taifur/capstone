# Reusable Skill: Disease Knowledge Database

DISEASES = {
    "rice_blast": {
        "name": "Rice Blast",
        "scientific_name": "Magnaporthe oryzae",
        "crop": "Rice",
        "pathogen_type": "Fungi",
        "symptoms": [
            "Diamond-shaped (spindle) lesions on leaves with gray or whitish centers and brown borders.",
            "Lesions can enlarge and coalesce, killing entire leaf blades.",
            "Can affect leaf sheaths, nodes, and panicles (causing neck blast and blanking of grains)."
        ],
        "environmental_factors": "Thrives in warm temperatures (25-28°C), high relative humidity (>90%), and prolonged leaf wetness (dew)."
    },
    "rice_bacterial_leaf_blight": {
        "name": "Bacterial Leaf Blight",
        "scientific_name": "Xanthomonas oryzae pv. oryzae",
        "crop": "Rice",
        "pathogen_type": "Bacteria",
        "symptoms": [
            "Wavy, yellowish to straw-colored stripes starting at the leaf margins or tips.",
            "Lesions extend along the veins and turn gray-white with age.",
            "Bacterial droplets (ooze) may form on the leaf surface under humid conditions."
        ],
        "environmental_factors": "Favored by temperatures of 25-34°C, high humidity, and wind-driven rain (which helps spread the bacteria)."
    },
    "potato_late_blight": {
        "name": "Potato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "crop": "Potato",
        "pathogen_type": "Oomycete (Fungus-like)",
        "symptoms": [
            "Water-soaked, irregular pale-green to dark-brown spots on leaves, often starting near leaf tips.",
            "In humid weather, a white, fuzzy mold growth appears on the undersides of infected leaves.",
            "Infected tubers show dry, reddish-brown rot."
        ],
        "environmental_factors": "Extremely active in cool (15-20°C), highly humid (relative humidity >85%), cloudy weather with frequent rainfall."
    },
    "tomato_leaf_curl": {
        "name": "Tomato Leaf Curl",
        "scientific_name": "Tomato leaf curl virus (TLCV)",
        "crop": "Tomato",
        "pathogen_type": "Virus (transmitted by Whitefly Vector)",
        "symptoms": [
            "Upward curling, puckering, and severe crinkling of leaves.",
            "Chlorosis (yellowing) of leaf margins and interveinal areas.",
            "Severe stunting of plant growth, with leaves appearing clustered and flowers dropping off before fruit set."
        ],
        "environmental_factors": "Most prevalent during dry, warm seasons when the whitefly vector (Bemisia tabaci) population is high."
    }
}

def search_disease_by_keyword(text: str) -> list[dict]:
    """Searches the database for crop diseases matching keywords in text."""
    matches = []
    text_lower = text.lower()
    for key, info in DISEASES.items():
        # Match crop name, disease name, or symptom keywords
        if (info["crop"].lower() in text_lower or 
            info["name"].lower() in text_lower or 
            any(sym.lower() in text_lower for sym in info["symptoms"])):
            matches.append(info)
    return matches

def get_disease_details(disease_key: str) -> dict:
    """Returns the full disease dictionary profile."""
    return DISEASES.get(disease_key)

def list_all_diseases() -> list[str]:
    """Returns a list of all supported crop diseases."""
    return [info["name"] for info in DISEASES.values()]
