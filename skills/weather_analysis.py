# Reusable Skill: Weather Advisory and Disease Risk Calculator

def calculate_disease_risks(temp: float, humidity: float) -> dict[str, str]:
    """
    Calculates disease risk levels based on temperature and relative humidity.
    Returns a dictionary of risks (e.g. {'potato_late_blight': 'High', ...})
    """
    risks = {
        "potato_late_blight": "Low",
        "rice_blast": "Low",
        "rice_bacterial_leaf_blight": "Low",
        "tomato_leaf_curl": "Low"
    }
    
    # 1. Potato Late Blight Risk (thrives in cool 15-22C and wet/humid >85% conditions)
    if 10 <= temp <= 22:
        if humidity >= 85:
            risks["potato_late_blight"] = "High"
        elif humidity >= 70:
            risks["potato_late_blight"] = "Medium"
            
    # 2. Rice Blast Risk (thrives in warm 25-30C and very wet/humid >90% conditions)
    if 24 <= temp <= 32:
        if humidity >= 90:
            risks["rice_blast"] = "High"
        elif humidity >= 80:
            risks["rice_blast"] = "Medium"
            
    # 3. Rice Bacterial Leaf Blight Risk (thrives in hot 25-34C and humid >80% conditions)
    if 25 <= temp <= 35:
        if humidity >= 80:
            risks["rice_bacterial_leaf_blight"] = "High"
        elif humidity >= 70:
            risks["rice_bacterial_leaf_blight"] = "Medium"
            
    # 4. Tomato Leaf Curl Risk (Whiteflies are highly active in dry/warm environments, low humidity)
    if temp >= 28 and humidity < 60:
        risks["tomato_leaf_curl"] = "High"
    elif temp >= 25 and humidity < 75:
        risks["tomato_leaf_curl"] = "Medium"
        
    return risks

def generate_weather_farming_advice(temp: float, humidity: float, rain_prob: float) -> list[str]:
    """Generates localized farming guidelines based on weather data."""
    advisories = []
    
    # Rain-based advisory
    if rain_prob >= 60:
        advisories.append("High probability of rain. POSTPONE all pesticide, fungicide, or fertilizer applications, as they are likely to wash away.")
        advisories.append("Ensure field drainage channels are cleared to prevent waterlogging, particularly in clayey crop beds.")
        advisories.append("If crops are near maturity, delay harvesting until the rain passes to prevent crop rot.")
    elif 30 <= rain_prob < 60:
        advisories.append("Unstable weather ahead with moderate rain probability. If spraying is critical, use a surfactant/sticker agent.")
    else:
        advisories.append("Low rain probability. Safe window for foliar sprays, harvesting, and field weeding.")
        
    # Temperature-based advisory
    if temp >= 35:
        advisories.append("Extreme heat alert! Apply light irrigation early in the morning or in the evening to reduce heat stress on crops.")
        advisories.append("Avoid manual field weeding or planting under direct sunlight during midday.")
    elif temp <= 15:
        advisories.append("Cool conditions. Monitor potato crops closely for dew condensation, which initiates late blight spore germination.")
        
    # Humidity-based advisory
    if humidity >= 85:
        advisories.append("High relative humidity increases disease spore propagation. Walk through fields and inspect leaf undersides for fungal fuzz.")
    elif humidity <= 50:
        advisories.append("Low relative humidity/dry air. Monitor for sucking pests like whiteflies, thrips, and mites which thrive in dry spells.")
        
    return advisories
