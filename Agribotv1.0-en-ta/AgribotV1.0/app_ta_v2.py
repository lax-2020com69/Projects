# english, tamil , responce for english ,tamil, tanlish

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --------------------
# Sri Lanka Agriculture Knowledge Base
# --------------------

REGIONAL_CROPS = {
    "wet zone": ["rice", "tea", "rubber", "banana", "vegetables"],
    "dry zone": ["maize", "chili", "groundnut", "cotton", "coconut"],
    "intermediate zone": ["rice", "maize", "vegetables", "coconut"],
}

PEST_CONTROL = {
    "rice": {
        "en": "You can use integrated pest management (IPM) including duck farming and Trichogramma wasps.",
        "ta": "நீங்கள் ஒருங்கிணைந்த பூச்சி மேலாண்மை (IPM) பயன்படுத்தலாம். அதில் வாத்து வளர்ப்பு மற்றும் Trichogramma பூச்சி நாசினிகள் உள்ளன.",
    },
    "tea": {
        "en": "Use pheromone traps and maintain shade trees to reduce pests.",
        "ta": "பூச்சிகளை குறைக்க Pheromone பந்துகள் மற்றும் நிழல் மரங்களை பராமரிக்கவும்.",
    },
    "vegetables": {
        "en": "Use neem oil spray and crop rotation for natural pest control.",
        "ta": "நீம் எண்ணெய் சிதைப்பு மற்றும் பயிர் மாறுதல் (crop rotation) இயற்கையான பூச்சி கட்டுப்பாடு.",
    },
}

SOIL_TYPES = {
    "red-yellow podzolic soil": {
        "en": "Found in wet and intermediate zones, suitable for tea and vegetables.",
        "ta": "ஈர மற்றும் இடைமட்ட மண்டலங்களில் காணப்படும், தேயில் மற்றும் காய்கறிகளுக்கு உகந்தது.",
    },
    "laterite soil": {
        "en": "Found in dry zone, suitable for chili, cotton and root crops.",
        "ta": "உலர் மண்டலத்தில் காணப்படும், மிளகாய், பருத்தி மற்றும் வெட்கிழங்கு பயிர்களுக்கு ஏற்றது.",
    },
    "alluvial soil": {
        "en": "Found near rivers and streams, best for rice cultivation.",
        "ta": "நதிகளின் அருகிலும் ஓடுகளிலும் காணப்படும், அரிசி பயிர்க்கு சிறந்தது.",
    },
}

FERTILIZER_ADVICE = {
    "rice": {
        "en": "Use urea and triple super phosphate (TSP) based on soil tests.",
        "ta": "மண் பரிசோதனை அடிப்படையில் யூரியா மற்றும் ட்ரிபிள் சூப்பர் பாஸ்பேட் (TSP) பயன்படுத்தவும்.",
    },
    "tea": {
        "en": "Carefully apply granular and nitrogen fertilizers.",
        "ta": "உருண்டிய பொருட்கள் மற்றும் நைட்ரஜன் உரங்களை கவனமாக பயன்படுத்தவும்.",
    },
    "vegetables": {
        "en": "Apply balanced NPK fertilizer and compost manure.",
        "ta": "சமமாக NPK உரம் மற்றும் கழிவு உரம் சேர்க்கவும்.",
    },
}

IRRIGATION_METHODS = {
    "wet zone": {
        "en": "Traditional canal irrigation and rain-fed methods.",
        "ta": "பாரம்பரிய கால்வாய் நீர்ப்பாசனம் மற்றும் மழை நம்பிய முறை.",
    },
    "dry zone": {
        "en": "Use tanks, wells, and drip irrigation to conserve water.",
        "ta": "குளங்கள், கிணறுகள் மற்றும் துளையடி நீர் பயன்பாடு நீர் சேமிப்பிற்கு.",
    },
}

SEASONAL_GUIDE = {
    "maha": {
        "en": "Main cropping season (October–March) with northeast monsoon rains.",
        "ta": "முக்கிய பயிரிடும் பருவம் (அக்டோபர்–மார்ச்), வடகிழக்கு பருவமழையுடன்.",
    },
    "yala": {
        "en": "Second cropping season (May–August) with southwest monsoon rains.",
        "ta": "இரண்டாவது பருவம் (மே–ஆகஸ்ட்), தென் மேற்கு பருவமழையுடன்.",
    },
}

# --------------------
# Intent Detection (English, Tamil, Tanglish)
# --------------------

def detect_intent(message):
    msg = message.lower()
    if any(word in msg for word in ["help", "உதவி", "udavi"]):
        return "help"
    elif any(word in msg for word in ["hi", "hello", "good morning", "good evening", "வணக்கம்", "vanakkam"]):
        return "greeting"
    elif any(word in msg for word in ["crop", "plant", "cultivate", "பயிர்", "payir"]):
        return "crop_info"
    elif any(word in msg for word in ["pest", "insect", "bug", "disease", "பூச்சி", "poochi"]):
        return "pest_info"
    elif any(word in msg for word in ["soil", "மண்", "man"]):
        return "soil_info"
    elif any(word in msg for word in ["fertilizer", "manure", "nutrient", "உரம்", "uram"]):
        return "fertilizer_info"
    elif any(word in msg for word in ["irrigation", "water", "நீர்ப்பாசனம்", "neerpasanam"]):
        return "irrigation_info"
    elif any(word in msg for word in ["season", "maha", "yala", "பருவம்", "paruvam"]):
        return "season_info"
    else:
        return "fallback"

# --------------------
# Language Detection (Basic heuristic)
# --------------------

def detect_language(message):
    # If contains Tamil unicode chars, consider Tamil; else English
    for ch in message:
        if '\u0B80' <= ch <= '\u0BFF':  # Tamil unicode range
            return 'ta'
    # Check some Tamil words written in English letters (Tanglish)
    # tamil_words = ["vanakkam", "payir", "poochi", "uram", "neerpasanam", "udavi", "paruvam", "man"]
    tamil_words = [
        "vanakkam", "payir", "poochi", "uram", "neerpasanam", "udavi", "paruvam", "man",
        "thanni", "meen", "madu", "kaasu", "kudam", "kaal", "vellam", "thirai", "kaatru",
        "mangai", "pookal", "maalai", "paal", "thengai", "siru", "manjal", "iravai",
        "paali", "thozhil", "muttu", "adi", "kaalam", "thulasi", "pani", "kootam",
        "valam", "vizhungi", "nell", "kizhangu"
    ]
    if any(word in message.lower() for word in tamil_words):
        return 'ta'
    # Otherwise default English
    return 'en'

# --------------------
# Response Generator (English or Tamil)
# --------------------

def get_response(intent, message, lang='en'):
    msg = message.lower()

    if intent == "greeting":
        if lang == 'ta':
            return "👋 வணக்கம்! நான் உங்கள் அக்ரிபாட் உதவியாளர். விவசாய உதவிக்கு `help` என டைப் செய்யவும்."
        else:
            return "👋 Hello! I am your AgriBot assistant. Type `help` for assistance."

    elif intent == "help":
        if lang == 'ta':
            return (
                "📋 நீங்கள் என்னை கேட்கலாம்:\n"
                "- ஈர, உலர், இடைமட்ட மண்டலங்களுக்கு ஏற்ற பயிர்கள்\n"
                "- பூச்சி கட்டுப்பாடு\n"
                "- இலங்கை மண் வகைகள்\n"
                "- உர பரிந்துரை\n"
                "- நீர்ப்பாசன முறைகள்\n"
                "- மகா மற்றும் யால பருவ விவசாயம்\n\n"
                "உதாரணம்: 'உலர் மண்டலத்தில் என்ன பயிர்கள்?'"
            )
        else:
            return (
                "📋 You can ask me about:\n"
                "- Crops suitable for wet, dry, and intermediate zones\n"
                "- Pest control methods\n"
                "- Soil types in Sri Lanka\n"
                "- Fertilizer recommendations\n"
                "- Irrigation methods\n"
                "- Maha and Yala seasonal farming\n\n"
                "Example: 'What crops grow in the dry zone?'"
            )

    elif intent == "crop_info":
        if "wet zone" in msg or "ஈர" in msg:
            crops = ", ".join(REGIONAL_CROPS.get("wet zone", []))
            if lang == 'ta':
                return f"🌾 ஈர மண்டல பயிர்கள்: {crops}."
            else:
                return f"🌾 Crops in the wet zone: {crops}."
        elif "dry zone" in msg or "உலர்" in msg:
            crops = ", ".join(REGIONAL_CROPS.get("dry zone", []))
            if lang == 'ta':
                return f"🌾 உலர் மண்டல பயிர்கள்: {crops}."
            else:
                return f"🌾 Crops in the dry zone: {crops}."
        elif "intermediate" in msg or "இடை" in msg:
            crops = ", ".join(REGIONAL_CROPS.get("intermediate zone", []))
            if lang == 'ta':
                return f"🌾 இடைமட்ட மண்டல பயிர்கள்: {crops}."
            else:
                return f"🌾 Crops in the intermediate zone: {crops}."
        else:
            if lang == 'ta':
                return "மண்டலத்தை குறிப்பிடவும்: ஈர, உலர், இடைமட்ட."
            else:
                return "Please specify zone: wet, dry, or intermediate."

    elif intent == "pest_info":
        for crop in PEST_CONTROL.keys():
            if crop in msg:
                if lang == 'ta':
                    return f"🐛 {crop.title()} க்கான பூச்சி கட்டுப்பாடு: {PEST_CONTROL[crop]['ta']}"
                else:
                    return f"🐛 Pest control for {crop.title()}: {PEST_CONTROL[crop]['en']}"
        if lang == 'ta':
            return "பயிர் பெயரை குறிப்பிடவும் (உதா: அரிசி, தேயிலை)."
        else:
            return "Please specify the crop (e.g., rice, tea)."

    elif intent == "soil_info":
        soils = ""
        for k, v in SOIL_TYPES.items():
            soils += f"- {k.title()}: {v[lang]}\n"
        if lang == 'ta':
            return f"🌱 இலங்கையில் காணப்படும் மண் வகைகள்:\n{soils}"
        else:
            return f"🌱 Soil types found in Sri Lanka:\n{soils}"

    elif intent == "fertilizer_info":
        for crop in FERTILIZER_ADVICE.keys():
            if crop in msg:
                if lang == 'ta':
                    return f"🌿 {crop.title()}க்கான உரம்: {FERTILIZER_ADVICE[crop]['ta']}"
                else:
                    return f"🌿 Fertilizer advice for {crop.title()}: {FERTILIZER_ADVICE[crop]['en']}"
        if lang == 'ta':
            return "பயிர் பெயரை குறிப்பிடவும்."
        else:
            return "Please specify the crop."

    elif intent == "irrigation_info":
        for zone in IRRIGATION_METHODS.keys():
            if zone in msg:
                if lang == 'ta':
                    return f"💧 {zone.title()} மண்டல நீர்ப்பாசன முறைகள்: {IRRIGATION_METHODS[zone]['ta']}"
                else:
                    return f"💧 Irrigation methods in the {zone} zone: {IRRIGATION_METHODS[zone]['en']}"
        if lang == 'ta':
            return "மண்டலத்தை (ஈர, உலர், இடைமட்ட) குறிப்பிடவும்."
        else:
            return "Please specify the zone (wet, dry, intermediate)."

    elif intent == "season_info":
        seasons = ""
        for k, v in SEASONAL_GUIDE.items():
            seasons += f"- {k.title()}: {v[lang]}\n"
        if lang == 'ta':
            return f"📅 பருவ வழிகாட்டி:\n{seasons}"
        else:
            return f"📅 Seasonal guide:\n{seasons}"

    else:
        if lang == 'ta':
            return "🤖 மன்னிக்கவும், புரியவில்லை. உதவிக்கு `help` என டைப் செய்யவும்."
        else:
            return "🤖 Sorry, I did not understand. Type `help` for assistance."

# --------------------
# Flask Routes
# --------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "").strip()

    lang = detect_language(user_msg)
    intent = detect_intent(user_msg)
    reply = get_response(intent, user_msg, lang)

    return jsonify({
        "response": reply,
        "language": lang,
        "intent": intent
    })

if __name__ == "__main__":
    app.run(debug=True)
