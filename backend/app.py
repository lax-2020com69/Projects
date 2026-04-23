# -------------------- Standard Library Modules --------------------
import os
import logging
import uuid
import json
import numpy as np
from PIL import Image

# -------------------- Flask and Web-related Modules --------------------
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# -------------------- ML & AI Modules --------------------
import tensorflow as tf
import google.generativeai as genai

# ------------------ Config ------------------
try:
    from config import GEMINI_API_KEY
except ImportError:
    GEMINI_API_KEY = "YOUR_API_KEY_HERE" 

MODEL_PATH = r"model\bestmodel\UWMAG_Image_classify.h5" 
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMG_HEIGHT, IMG_WIDTH = 180, 180
CLASS_NAMES = ['Cardboard', 'can', 'glass', 'paper', 'plastic']

LANG_MAP = {
    "en": "English",
    "ta": "Tamil",
    "si": "Sinhala"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.INFO)
tf.get_logger().setLevel(logging.ERROR)

# ------------------ AI Model Setup ------------------
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    logging.info("✅ CNN Model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Failed to load model at {MODEL_PATH}: {e}")
    model = None

# ------------------ Utility Functions ------------------

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prepare_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = tf.expand_dims(image_array, 0)
    return image_array

# 💡 UPDATED Gemini DIY generator
def generate_diy_ideas(waste_type, lang_code="en"):
    """Generates 5 high-quality, stylized DIY ideas in the requested language."""
    
    language_name = LANG_MAP.get(lang_code, "English")

    # Updated prompt to force the "✨" and "🛠️" style and detailed descriptions
    prompt = f"""
    You are a creative DIY expert. 
    Material: {waste_type}
    Language: {language_name}

    Task:
    Generate 5 beginner-friendly, high-quality DIY project ideas using {waste_type}.
    
    Style Guidelines:
    1. Titles must start with the ✨ emoji.
    2. Descriptions should be detailed, encouraging, and professional (not just one sentence).
    3. Preparations should be a comprehensive list of materials needed.
    4. All content MUST be in {language_name}.

    Output Rules:
    - Return ONLY valid JSON.
    - Do NOT include markdown blocks (like ```json).
    - JSON Format:
    [
      {{
        "title": "✨ [Idea Name]",
        "description": "[Detailed explanation of how to make it and what it's used for]",
        "preparations": ["item 1", "item 2", "item 3"]
      }}
    ]
    """

    try:
        response = gemini_model.generate_content(prompt)
        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        ideas = json.loads(text)
        if isinstance(ideas, list):
            return ideas
    except Exception as e:
        print("Gemini Error:", e)

    # 🛠️ UPDATED Fallback: Now matches your requested high-quality format
    return [
        {
            "title": f"✨ Decorative {waste_type} Organizer", 
            "description": f"Transform an empty, clean {waste_type} into a personalized desk organizer by decorating its exterior with paper, fabric, or paint to hold stationery.", 
            "preparations": [f"Empty {waste_type} (cleaned)", "Craft paper or paint", "Glue", "Scissors"]
        },
        {
            "title": f"✨ Eco-Friendly {waste_type} Planter", 
            "description": f"Convert a clean {waste_type} into a charming small planter for herbs or succulents. Ensure you add drainage holes at the bottom.", 
            "preparations": [f"Empty {waste_type} (cleaned)", "Potting soil", "Small plant or seeds", "Nail and hammer for holes"]
        },
        {
            "title": f"✨ Creative {waste_type} Home Decor", 
            "description": f"Turn your {waste_type} waste into a beautiful home ornament or candle holder to add a touch of recycled art to your living room.", 
            "preparations": [f"Empty {waste_type}", "Acrylic paints", "Paintbrushes", "Decorative glitter or ribbon"]
        },
        {
            "title": f"✨ Upcycled {waste_type} Gift Box", 
            "description": f"Decorate an empty {waste_type} to make a unique, reusable gift container for small presents, candies, or party favors.", 
            "preparations": [f"Empty {waste_type}", "Gift wrap or colorful paper", "Ribbon", "Glue"]
        },
        {
            "title": f"✨ DIY {waste_type} Toy for Kids", 
            "description": f"Build a simple, imaginative toy for children using {waste_type}, encouraging creativity and environmental awareness through play.", 
            "preparations": [f"Empty {waste_type}", "Strong string", "Bright colors/markers", "Safety tape"]
        }
    ]

# ------------------ API Routes ------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "UWMAG Backend is running!"}), 200

@app.route("/uploads/<path:filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded on server"}), 500

    file = request.files.get("file") or request.files.get("image")
    lang_code = request.form.get("language", "en")

    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Upload JPG/PNG."}), 400

    try:
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        image_tensor = prepare_image(filepath)
        predictions = model.predict(image_tensor)
        score = tf.nn.softmax(predictions[0])
        
        predicted_label = CLASS_NAMES[np.argmax(score)]
        confidence = round(float(np.max(score)) * 100, 2)

        diy_ideas = generate_diy_ideas(predicted_label, lang_code)

        return jsonify({
            "label": predicted_label,
            "confidence": confidence,
            "file_url": f"/uploads/{filename}",
            "diy_ideas": diy_ideas
        })

    except Exception as e:
        logging.error(f"❌ Prediction failed: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True, use_reloader=False)
