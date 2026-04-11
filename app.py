from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import json

app = Flask(__name__)

# Load Model and Class Names
model = tf.keras.models.load_model('model.h5')
with open('classes.txt', 'r') as f:
    class_names = f.read().splitlines()

# Load Nutrition Data
def load_nutrition_data():
    with open('nutrition.json', 'r') as f:
        data = json.load(f)
        return data['nutrition_data']

# --- NEW: Load Food/Dishes Data ---
def load_food_data():
    with open('food.json', 'r') as f:
        data = json.load(f)
        return data['foods']

nutrition_db = load_nutrition_data()
food_db = load_food_data() # Initialize food database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    file = request.files['file']
    filepath = os.path.join('static', file.filename)
    file.save(filepath)

    # Preprocess image
    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Predict
    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions)
    result = class_names[class_idx]
    confidence = float(np.max(predictions))

    # Search for nutrition data
    nutrition_info = next((item for item in nutrition_db if item["name"].lower() == result.lower()), None)
    
    # --- NEW: Search for dishes data ---
    food_info = next((item for item in food_db if item["name"].lower() == result.lower()), None)
    dishes_list = food_info["dishes"] if food_info else []

    return jsonify({
        'prediction': result, 
        'confidence': f"{confidence*100:.2f}%",
        'nutrition': nutrition_info, 
        'dishes': dishes_list, # Pass the list of 5 dishes
        'image_path': filepath
    })

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
