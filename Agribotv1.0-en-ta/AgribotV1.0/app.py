# english to english responce

from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# --------------------
# Sri Lanka specific agriculture knowledge base
# --------------------

REGIONAL_CROPS = {
    "wet zone": [
        "rice", "tea", "rubber", "banana", "vegetables",
        "pepper", "clove", "nutmeg", "cinnamon", "ginger",
        "taro", "jackfruit", "mango", "pineapple"
    ],
    "dry zone": [
        "maize", "chili", "groundnut", "cotton", "coconut",
        "millet", "sorghum", "onion", "mung bean", "black gram",
        "cowpea", "sesame", "tobacco", "palmyra", "cassava"
    ],
    "intermediate zone": [
        "rice", "maize", "vegetables", "coconut",
        "banana", "papaya", "pineapple", "ginger",
        "tobacco", "peanut", "sugarcane", "green gram"
    ]
}

PEST_CONTROL = {
    "rice": "Use integrated pest management (IPM) including duck farming and biological controls like Trichogramma wasps.",
    "tea": "Use pheromone traps and maintain shade trees to reduce pests.",
    "vegetables": "Neem oil spray and crop rotation are effective organic pest controls.",
    "banana": "Remove and destroy infected suckers; use pheromone traps for banana weevils and apply neem-based products.",
    "maize": "Use Trichogramma wasps to control stem borers and practice crop rotation.",
    "chili": "Use yellow sticky traps for aphids and whiteflies; neem seed kernel extract (NSKE) spray is effective.",
    "groundnut": "Seed treatment with fungicides and application of neem cake help control early pests and soil-borne diseases.",
    "coconut": "Use biological control for rhinoceros beetles (Oryctes rhinoceros nudivirus) and install light traps.",
    "rubber": "Regular removal of diseased leaves and fungicidal spraying helps manage fungal pests like powdery mildew.",
    "pepper": "Apply Bordeaux mixture to control fungal infections and use neem oil spray to manage insects.",
    "onion": "Use light traps for cutworms and avoid monocropping to reduce pest buildup.",
    "mung bean": "Use intercropping with maize and apply NSKE to reduce aphid infestation.",
}

SOIL_TYPES = {
    "red-yellow podzolic soil": "Common in wet and intermediate zones, suitable for tea, rubber, coconut, and vegetables.",
    "laterite soil": "Found in the dry zone and some parts of the intermediate zone, suitable for chili, cotton, groundnut, and pulses.",
    "alluvial soil": "Found along river valleys and floodplains, especially in the dry zone; ideal for rice, vegetables, and other field crops.",
    "rendzinas": "Shallow soils over limestone, mostly in the Jaffna peninsula; suitable for tobacco, onion, and legumes.",
    "grumusol (black soil)": "Found in parts of the North Central and Northern provinces; good for paddy, onion, and pulses.",
    "lithosols": "Shallow soils over hard rock in hilly and mountainous areas; limited cultivation, but used for forestry and tea in some areas.",
    "peat soil": "Found in low-lying, marshy areas (e.g., Muthurajawela); suitable for certain wetland crops and paddy with proper drainage.",
    "reddish brown earth": "Typical in the dry and intermediate zones; suitable for paddy, maize, banana, and sugarcane.",
}

FERTILIZER_ADVICE = {
    "rice": "Apply Urea and Triple Superphosphate (TSP) according to soil test recommendations; Muriate of Potash (MOP) may be added during tillering.",
    "tea": "Use nitrogen-based fertilizers like Urea in split doses; supplement with compost and maintain soil pH with dolomite lime as needed.",
    "vegetables": "Apply a balanced NPK (e.g., 10:10:10) fertilizer; incorporate organic compost or farmyard manure for improved soil structure.",
    "banana": "Apply well-rotted manure before planting; use NPK (3:1:6) during growth stages and increase potassium during fruiting.",
    "maize": "Apply Urea, TSP, and MOP in a 2:1:1 ratio based on soil testing; top dress with Urea during the knee-high and tasseling stages.",
    "chili": "Use a balanced NPK fertilizer like 5:15:45; apply compost at land preparation and use foliar sprays of micronutrients if needed.",
    "groundnut": "Apply gypsum for calcium; use a basal dose of TSP and MOP, and apply compost or green manure for soil enrichment.",
    "coconut": "Apply a mixture of Urea, TSP, and MOP (e.g., 1:1:2) annually; supplement with magnesium sulfate (kieserite) and organic mulch.",
    "rubber": "Apply rock phosphate and compost in the early stages; use NPK (especially potassium) for mature trees, and lime to correct soil acidity.",
    "onion": "Use a starter dose of compost; apply NPK in 2:1:2 ratio, and add micronutrients like zinc if deficiencies are observed.",
    "mung bean": "Use Rhizobium inoculation for nitrogen fixation; apply phosphorus (TSP) and potassium as needed, with minimal nitrogen input.",
}

IRRIGATION_METHODS = {
    "wet zone": "Traditional canal irrigation and rain-fed systems are predominant due to high annual rainfall. Small streams and gravity-based irrigation are also common.",
    "dry zone": "Tanks (wewas), wells, and drip irrigation are widely used to conserve water. Large-scale irrigation systems like the Mahaweli project also support paddy and field crops.",
    "intermediate zone": "Combines both rain-fed and irrigation methods. Small tanks, lift irrigation, and sprinkler systems are used depending on topography and crop type.",
}

SEASONAL_GUIDE = {
    "maha": "Main cultivation season (October to March), coinciding with the northeast monsoon. Suitable for paddy and most field crops due to abundant rainfall.",
    "yala": "Secondary cultivation season (May to August), associated with the southwest monsoon. Requires irrigation in many areas, commonly used for short-duration crops and vegetables.",
    "inter-seasonal": "Short periods between Yala and Maha (March-April and September) used for land preparation, minor crop cultivation, or fallowing. In some regions, vegetables and legumes are planted.",
}

# --------------------
# Intent detection with regional understanding
# --------------------

def detect_intent(message):
    msg = message.lower()
    if "help" in msg:
        return "help"
    elif any(greet in msg for greet in ["hey", "hello", "good morning", "good evening"]):
        return "greeting"
    elif "hi"== msg:
        return "greeting"
    elif any(word in msg for word in ["crop", "plant", "cultivate", "harvest"]):
        return "crop_info"
    elif any(word in msg for word in ["pest", "insect", "bug", "disease", "infestation"]):
        return "pest_info"
    elif "soil" in msg or "land" in msg:
        return "soil_info"
    elif any(word in msg for word in ["fertilizer", "manure", "nutrient", "compost"]):
        return "fertilizer_info"
    elif any(word in msg for word in ["irrigation", "water", "drip", "sprinkler"]):
        return "irrigation_info"
    elif any(word in msg for word in ["season", "maha", "yala", "inter-seasonal", "harvest time"]):
        return "season_info"
    elif any(word in msg for word in ["time", "date", "current time", "week"]):
        return "time_info"
    else:
        return "fallback"

def get_response(intent, message):
    msg = message.lower()

    if intent == "time_info":
        now = datetime.datetime.now()
        formatted = now.strftime("%A, %d %B %Y %I:%M %p")
        return f"⏰ Current Date & Time in Sri Lanka: {formatted}"

    
    if intent == "greeting":
        return "👋 Hello from AgriBot Sri Lanka! I’m here to help with farming tips for your region. Type `help` to see what I can do."
    
    if intent == "help":
        return (
            "📋 You can ask me about:\n"
            "- Best crops for Wet, Dry, or Intermediate zones\n"
            "- Pest control methods for common crops\n"
            "- Soil types in Sri Lanka and suitable crops\n"
            "- Fertilizer usage and recommendations\n"
            "- Irrigation methods specific to Sri Lankan zones\n"
            "- Maha and Yala seasonal farming tips\n\n"
            "Try: 'What crops grow in the dry zone?' or 'Pest control for rice in Sri Lanka?'"
        )
    
    if intent == "crop_info":
        # Check for zone keyword
        if "wet zone" in msg or "wet" in msg:
            crops = ", ".join(REGIONAL_CROPS["wet zone"])
            return f"🌾 Wet Zone Crops: {crops}. Ideal for tea, rubber, and rice."
        elif "dry zone" in msg or "dry" in msg:
            crops = ", ".join(REGIONAL_CROPS["dry zone"])
            return f"🌾 Dry Zone Crops: {crops}. Best suited for chili, maize, and coconut."
        elif "intermediate zone" in msg or "intermediate" in msg:
            crops = ", ".join(REGIONAL_CROPS["intermediate zone"])
            return f"🌾 Intermediate Zone Crops: {crops}."
        else:
            return (
                "Please specify the zone: Wet Zone, Dry Zone, or Intermediate Zone to get crop info."
            )
    
    if intent == "pest_info":
        for crop in PEST_CONTROL.keys():
            if crop in msg:
                return f"🐛 Pest Control for {crop.title()}: {PEST_CONTROL[crop]}"
        return "Please specify the crop name for pest control advice (e.g., rice, tea, vegetables)."
    
    if intent == "soil_info":
        soils = "\n".join([f"- {k.title()}: {v}" for k, v in SOIL_TYPES.items()])
        return f"🌱 Common Soil Types in Sri Lanka:\n{soils}"
    
    if intent == "fertilizer_info":
        for crop in FERTILIZER_ADVICE.keys():
            if crop in msg:
                return f"🌿 Fertilizer Tips for {crop.title()}: {FERTILIZER_ADVICE[crop]}"
        return "Please specify a crop for fertilizer recommendations (e.g., rice, tea, vegetables)."
    
    if intent == "irrigation_info":
        for zone in IRRIGATION_METHODS.keys():
            if zone in msg:
                return f"💧 Irrigation in {zone.title()}: {IRRIGATION_METHODS[zone]}"
        return (
            "Irrigation methods vary by zone. Mention your zone (wet, dry, intermediate) "
            "to get specific advice."
        )
    
    if intent == "season_info":
        seasons = "\n".join([f"- {k.title()}: {v}" for k, v in SEASONAL_GUIDE.items()])
        return f"📅 Sri Lanka Seasonal Guide:\n{seasons}\n\nMaha season is Oct-Mar, Yala is May-Aug."
    
    # fallback response
    return (
        "🤖 Sorry, I didn’t quite understand. Ask me about Sri Lankan crops, pests, soil, fertilizers, irrigation, or seasonal tips."
    )

# --------------------
# Flask Routes
# --------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    intent = detect_intent(user_msg)
    reply = get_response(intent, user_msg)
    return jsonify({"response": reply})

# --------------------
# Run
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
