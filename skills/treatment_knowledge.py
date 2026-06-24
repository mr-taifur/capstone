# Reusable Skill: Treatment Recommendation Database

TREATMENTS = {
    "rice_blast": {
        "disease_name": "Rice Blast",
        "organic": [
            "Seed treatment: Soak seeds in warm water (54°C) for 15 minutes before sowing.",
            "Avoid excess nitrogen fertilizers, which favor vegetative growth and enhance disease severity.",
            "Implement crop rotation with non-host crops (e.g., legumes) in the next season."
        ],
        "biological": [
            "Apply formulations of Trichoderma harzianum or Pseudomonas fluorescens as seed treatments or foliar sprays."
        ],
        "chemical": [
            "Apply Tricyclazole (e.g., Trooper 75 WP) at 0.75g/L of water or Tebuconazole + Trifloxystrobin (e.g., Nativo 75 WG) at 0.6g/L of water.",
            "Apply at first sign of leaf blast or before panicle emergence if weather is humid and cloudy."
        ],
        "safety_notes": "Wear protective gear (mask, gloves) when spraying fungicides. Keep a 14-day pre-harvest interval (PHI) after chemical application."
    },
    "rice_bacterial_leaf_blight": {
        "disease_name": "Bacterial Leaf Blight",
        "organic": [
            "Practice balanced fertilizer application: split nitrogen applications and ensure sufficient Potassium (Potash/MOP).",
            "Drain infected fields for 3-4 days to reduce moisture, as the bacteria spread in standing water.",
            "Keep field borders clean of weeds that can host the bacteria."
        ],
        "biological": [
            "Currently, biological controls are mostly preventive. Spraying cow dung slurry extract (diluted) is sometimes used locally to create a competitive microflora."
        ],
        "chemical": [
            "Foliar spray of Copper Oxychloride (e.g., Cupravit 50 WP) at 2g/L of water combined with Streptocycline or Bismerthiazol.",
            "Avoid spraying during high noon or heavy wind. Spray in late afternoon."
        ],
        "safety_notes": "Copper compounds can irritate eyes. Wash hands thoroughly. Ensure no rain is expected for at least 4 hours post-spraying."
    },
    "potato_late_blight": {
        "disease_name": "Potato Late Blight",
        "organic": [
            "Plant only certified, disease-free seed tubers.",
            "Ensure proper earthing up to cover tubers and prevent spores washing down from leaves.",
            "Promptly harvest and remove/burn infected vines (dehaulming) 2 weeks before harvesting tubers."
        ],
        "biological": [
            "Apply Trichoderma viride or Bacillus subtilis to the soil at planting time to compete with oomycetes."
        ],
        "chemical": [
            "Preventive: Spray Mancozeb (e.g., Dithane M-45) at 2g/L of water weekly when weather becomes cloudy and foggy.",
            "Curative: If symptoms appear, spray Metalaxyl + Mancozeb (e.g., Ridomil Gold) or Fenamidone + Mancozeb (e.g., Secure) at 2g/L of water."
        ],
        "safety_notes": "Mancozeb is toxic to aquatic life. Do not spray near water bodies or fish ponds. Observe a 14-day pre-harvest interval."
    },
    "tomato_leaf_curl": {
        "disease_name": "Tomato Leaf Curl (TLCV)",
        "organic": [
            "Set up yellow sticky traps (1 trap per 10-15 plants) to monitor and capture the whitefly vector.",
            "Use nylon mesh nets (40-50 mesh) in nurseries to prevent whiteflies from infecting young seedlings.",
            "Uproot and destroy infected plants early to prevent them from serving as virus reservoirs."
        ],
        "biological": [
            "Spray Neem Oil (5ml/L of water) mixed with a few drops of liquid soap. Neem oil acts as a natural whitefly repellant and anti-feedant."
        ],
        "chemical": [
            "Spray Imidacloprid (e.g., Admire 200 SL) at 0.5ml/L of water or Acetamiprid (e.g., Tundra 20 SP) at 0.5g/L of water to control the whitefly vectors.",
            "Alternate chemical classes to prevent insect resistance development."
        ],
        "safety_notes": "Imidacloprid is highly toxic to bees. Avoid spraying when crops are in full bloom or when bees are actively foraging. Spray in the evening."
    }
}

def get_treatment_recs(disease_key: str) -> dict:
    """Returns the organic, biological, and chemical treatment guidelines for a disease."""
    return TREATMENTS.get(disease_key)
