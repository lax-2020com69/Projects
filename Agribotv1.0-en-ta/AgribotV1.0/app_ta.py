# english ,tamil query to english responce

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --------------------
# Sri Lanka specific agriculture knowledge base
# --------------------

REGIONAL_CROPS = {
    "wet zone": ["rice", "tea", "rubber", "banana", "vegetables"],
    "dry zone": ["maize", "chili", "groundnut", "cotton", "coconut"],
    "intermediate zone": ["rice", "maize", "vegetables", "coconut"],
}

PEST_CONTROL = {
    "rice": "Use integrated pest management (IPM) including duck farming and biological controls like Trichogramma wasps.",
    "tea": "Use pheromone traps and maintain shade trees to reduce pests.",
    "vegetables": "Neem oil spray and crop rotation are effective organic pest controls.",
}

SOIL_TYPES = {
    "red-yellow podzolic soil": "Common in wet and intermediate zones, suitable for tea and vegetables.",
    "laterite soil": "Found in dry zone, suitable for chili, cotton, and groundnut.",
    "alluvial soil": "Found along rivers and delta, good for rice cultivation.",
}

FERTILIZER_ADVICE = {
    "rice": "Apply Urea and Triple Superphosphate (TSP) according to soil test recommendations.",
    "tea": "Use organic matter and nitrogen fertilizers carefully to maintain soil health.",
    "vegetables": "Use balanced NPK and add compost regularly.",
}

IRRIGATION_METHODS = {
    "wet zone": "Traditional canal irrigation and rain-fed systems are predominant.",
    "dry zone": "Tanks, wells, and drip irrigation are common to conserve water.",
}

SEASONAL_GUIDE = {
    "maha": "Main cultivation season (Oct-Mar) with rains from northeast monsoon.",
    "yala": "Secondary season (May-Aug) with southwest monsoon rains.",
}

# --------------------
# Intent detection with regional understanding
# --------------------

def detect_intent(message):
    msg = message.lower()
    if "help" in msg or "உதவி" in msg:
        return "help"
    elif any(greet in msg for greet in ["hi", "hello", "good morning", "good evening", "வணக்கம்"]):
        return "greeting"
    elif any(word in msg for word in ["crop", "plant", "cultivate", "பயிர்"]):
        return "crop_info"
    elif any(word in msg for word in ["pest", "insect", "bug", "disease", "பூச்சி"]):
        return "pest_info"
    elif "soil" in msg or "மண்" in msg:
        return "soil_info"
    elif any(word in msg for word in ["fertilizer", "manure", "nutrient", "உரம்"]):
        return "fertilizer_info"
    elif "irrigation" in msg or "water" in msg or "நீர்ப்பாசனம்" in msg:
        return "irrigation_info"
    elif any(word in msg for word in ["season", "maha", "yala", "பருவம்"]):
        return "season_info"
    else:
        return "fallback"

# --------------------
# Get Response (English & Tamil Support)
# --------------------

def get_response(intent, message, lang='en'):
    msg = message.lower()

    if lang == 'ta':  # Tamil responses
        if intent == "greeting":
            return "👋 வணக்கம்! நான் உங்கள் அக்ரிபாட் உதவியாளர். விவசாய உதவிக்கு `help` என تایப் செய்யவும்."
        elif intent == "help":
            return (
                "📋 நீங்கள் என்னை கேட்கலாம்:\n"
                "- ஈர, உலர், இடைமட்ட மண்டலங்களுக்கு ஏற்ற பயிர்கள்\n"
                "- பூச்சி கட்டுப்பாடு\n"
                "- இலங்கை மண் வகைகள்\n"
                "- உரம் பரிந்துரை\n"
                "- நீர்ப்பாசன முறைகள்\n"
                "- மகா மற்றும் யால பருவ விவசாயம்\n\n"
                "உதாரணம்: 'உலர் மண்டலத்தில் என்ன பயிர்கள்?'"
            )
        elif intent == "crop_info":
            if "wet zone" in msg or "ஈர" in msg:
                crops = ", ".join(REGIONAL_CROPS["wet zone"])
                return f"🌾 ஈர மண்டல பயிர்கள்: {crops}."
            elif "dry zone" in msg or "உலர்" in msg:
                crops = ", ".join(REGIONAL_CROPS["dry zone"])
                return f"🌾 உலர் மண்டல பயிர்கள்: {crops}."
            elif "intermediate" in msg or "இடை" in msg:
                crops = ", ".join(REGIONAL_CROPS["intermediate zone"])
                return f"🌾 இடைமட்ட மண்டல பயிர்கள்: {crops}."
            else:
                return "மண்டலத்தை குறிப்பிடவும்: ஈர, உலர், இடைமட்ட."
        elif intent == "pest_info":
            for crop in PEST_CONTROL.keys():
                if crop in msg:
                    return f"🐛 {crop.title()} க்கான பூச்சி கட்டுப்பாடு: {PEST_CONTROL[crop]}"
            return "பயிர் பெயரை குறிப்பிடவும் (உதா: அரிசி, தேயிலை)."
        elif intent == "soil_info":
            soils = "\n".join([f"- {k.title()}: {v}" for k, v in SOIL_TYPES.items()])
            return f"🌱 இலங்கையில் காணப்படும் மண் வகைகள்:\n{soils}"
        elif intent == "fertilizer_info":
            for crop in FERTILIZER_ADVICE.keys():
                if crop in msg:
                    return f"🌿 {crop.title()}க்கான உரம்: {FERTILIZER_ADVICE[crop]}"
            return "பயிர் பெயரை குறிப்பிடவும்."
        elif intent == "irrigation_info":
            for zone in IRRIGATION_METHODS.keys():
                if zone in msg:
                    return f"💧 {zone.title()} மண்டல நீர்ப்பாசன முறைகள்: {IRRIGATION_METHODS[zone]}"
            return "மண்டலத்தை (ஈர, உலர், இடைமட்ட) குறிப்பிடவும்."
        elif intent == "season_info":
            seasons = "\n".join([f"- {k.title()}: {v}" for k, v in SEASONAL_GUIDE.items()])
            return f"📅 பருவ வழிகாட்டி:\n{seasons}"
        return "🤖 மன்னிக்கவும், புரியவில்லை. உதவிக்கு `help` என تایப் செய்யவும்."

    # Default English
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
            "Try: 'What crops grow in the dry zone?'"
        )

    if intent == "crop_info":
        if "wet zone" in msg:
            crops = ", ".join(REGIONAL_CROPS["wet zone"])
            return f"🌾 Wet Zone Crops: {crops}. Ideal for tea, rubber, and rice."
        elif "dry zone" in msg:
            crops = ", ".join(REGIONAL_CROPS["dry zone"])
            return f"🌾 Dry Zone Crops: {crops}. Best suited for chili, maize, and coconut."
        elif "intermediate" in msg:
            crops = ", ".join(REGIONAL_CROPS["intermediate zone"])
            return f"🌾 Intermediate Zone Crops: {crops}."
        else:
            return "Please specify the zone: Wet Zone, Dry Zone, or Intermediate Zone."

    if intent == "pest_info":
        for crop in PEST_CONTROL.keys():
            if crop in msg:
                return f"🐛 Pest Control for {crop.title()}: {PEST_CONTROL[crop]}"
        return "Please specify the crop name for pest control advice (e.g., rice, tea)."

    if intent == "soil_info":
        soils = "\n".join([f"- {k.title()}: {v}" for k, v in SOIL_TYPES.items()])
        return f"🌱 Common Soil Types in Sri Lanka:\n{soils}"

    if intent == "fertilizer_info":
        for crop in FERTILIZER_ADVICE.keys():
            if crop in msg:
                return f"🌿 Fertilizer Tips for {crop.title()}: {FERTILIZER_ADVICE[crop]}"
        return "Please specify a crop for fertilizer recommendations."

    if intent == "irrigation_info":
        for zone in IRRIGATION_METHODS.keys():
            if zone in msg:
                return f"💧 Irrigation in {zone.title()}: {IRRIGATION_METHODS[zone]}"
        return "Mention your zone (wet, dry, intermediate) to get irrigation advice."

    if intent == "season_info":
        seasons = "\n".join([f"- {k.title()}: {v}" for k, v in SEASONAL_GUIDE.items()])
        return f"📅 Sri Lanka Seasonal Guide:\n{seasons}"

    return "🤖 Sorry, I didn’t quite understand. Ask me about Sri Lankan crops, pests, soil, fertilizers, or seasonal tips."


# --------------------
# Flask Routes
# --------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    lang = data.get("lang", "en")  # 'en' or 'ta'
    intent = detect_intent(user_msg)
    reply = get_response(intent, user_msg, lang)
    return jsonify({"response": reply})

# --------------------
# Run App
# --------------------

if __name__ == "__main__":
    app.run(debug=True)
