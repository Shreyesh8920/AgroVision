

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import pickle
import logging
import pandas as pd
import numpy as np
import uuid
from services.weather_api import get_weather
from services.geocoding import geocode
from services.soil_api import get_soil
from services.chat import chat_engine,clear_context


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmdata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

crop_cache = {}
fertilizer_cache = {}
yield_model_cache = {}

class FarmData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    soil_type = db.Column(db.String(50))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/crop")
def crop_page():
    return render_template("crop.html")

@app.route("/yield")
def yield_page():
    return render_template("yield.html")

@app.route("/fertiliser")
def fertiliser_page():
    return render_template("fertiliser.html")

@app.route("/chat")
def chat_page():
    return render_template("chat.html")
# @app.route("/learn")
# def learn_page():
#     return render_template("learn6.html")

@app.route("/collect", methods=["GET"])
def collect():
    location = request.args.get("location")
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if location:
        lat, lon = geocode(location)

    if not lat or not lon:
        return jsonify({"error": "Invalid location"}), 400

    weather = get_weather(lat, lon)
    soil = get_soil(lat, lon)

    if isinstance(soil, dict):
        soil_type = soil.get("soil_type") or soil.get("error") or "Unknown"
    else:
        soil_type = str(soil)

    record = FarmData(
    location=location or "GPS",
    temperature=weather["temperature"],
    humidity=weather["humidity"],
    rainfall=weather["rainfall"],
    wind_speed=weather["wind_speed"],
    soil_type=soil_type
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "rainfall": weather["rainfall"],
        "wind_speed": weather["wind_speed"],
        "soil_type": soil
    })

def load_crop_rec_model():
    if not crop_cache:
        model_path = MODELS_DIR / "crop_recommendation_pipeline.pkl"
        with model_path.open("rb") as f:
            objs = pickle.load(f)
            crop_cache.update(objs)
    return crop_cache


@app.route("/recommend_crop", methods=["POST"])
def recommend_crop():
    data = request.json
    print("CROP_RECC DATA: ",request.json)
    model_objs = load_crop_rec_model()

    df = pd.DataFrame([data])
    X_scaled = model_objs["scaler"].transform(df)
    pred = model_objs["model"].predict(X_scaled)[0]
    crop = model_objs["label_encoder"].inverse_transform([pred])[0]

    return jsonify({"recommended_crop": crop})

def load_fertilizer_model():
    if not fertilizer_cache:
        model_path = MODELS_DIR / "fertilizer_model_pipeline.pkl"
        with model_path.open("rb") as f:
            objs = pickle.load(f)
            fertilizer_cache.update(objs)
    return fertilizer_cache


@app.route('/recommend_fertilizer', methods=['POST'])
def recommend_fertilizer():
    data = request.json
    print("FERTILIZER INPUT FROM UI:", data)

    model_objs = load_fertilizer_model()

    try:
        required_fields = [
            'Nitrogen', 'Phosphorous', 'Potassium', 'PH',
            'Temperature', 'Moisture', 'Rainfall', 'Carbon',
            'Crop', 'Soil'
        ]

        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({'error': f'Missing required fields: {missing}'}), 400

        df_input = pd.DataFrame([data])

        if df_input.at[0, 'Crop'] not in model_objs['le_crop'].classes_:
            return jsonify({'error': 'Unsupported crop value'}), 400

        if df_input.at[0, 'Soil'] not in model_objs['le_soil'].classes_:
            return jsonify({'error': 'Unsupported soil value'}), 400

        df_input['Crop_le'] = model_objs['le_crop'].transform(df_input['Crop'])
        df_input['Soil_le'] = model_objs['le_soil'].transform(df_input['Soil'])

        numeric_cols = [
            'Nitrogen', 'Phosphorous', 'Potassium', 'PH',
            'Temperature', 'Moisture', 'Rainfall', 'Carbon'
        ]

        df_input[numeric_cols] = model_objs['scaler'].transform(
            df_input[numeric_cols]
        )

        feature_order = numeric_cols + ['Crop_le', 'Soil_le']
        X = df_input[feature_order]

        pred_encoded = model_objs['model'].predict(X)[0]
        pred_fert = model_objs['le_fert'].inverse_transform([pred_encoded])[0]

        return jsonify({'recommended_fertilizer': pred_fert})

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 400

def load_yield_model_and_encoders(crop_name):
    crop_name = crop_name.lower().strip()

    model_path = MODELS_DIR / f"gb_model_{crop_name}.pkl"
    encoder_path = MODELS_DIR / f"label_encoders_{crop_name}.pkl"

    if not model_path.exists() or not encoder_path.exists():
        logging.error(f"No model or encoders found for crop: {crop_name}")
        return None, None

    with model_path.open("rb") as f:
        model = pickle.load(f)

    with encoder_path.open("rb") as f:
        encoders = pickle.load(f)

    return model, encoders


@app.route("/predict_yield", methods=["POST"])
def predict_yield():
    data = request.json
    print("YIELD INPUT FROM UI:", data)

    if not data or "crop_name" not in data:
        return jsonify({"error": "crop_name is required"}), 400

    crop_name = data["crop_name"].lower()

    input_features = {k: v for k, v in data.items() if k != "crop_name"}

    for col in ["Fertilizer_Used", "Irrigation_Used"]:
        if col in input_features:
            val = input_features[col]
            if isinstance(val, list):
                raw_val = val[0] if val else None
                if isinstance(raw_val, str):
                    input_features[col][0] = raw_val.strip().lower() == "true"
            elif isinstance(val, str):
                input_features[col] = val.strip().lower() == "true"

    df_input = pd.DataFrame({
        k: v if isinstance(v, list) else [v]
        for k, v in input_features.items()
    })

    model, label_encoders = load_yield_model_and_encoders(crop_name)
    if model is None or label_encoders is None:
        logging.error(f"No model found for crop: {crop_name}")
        return jsonify({"error": f'No model found for crop "{crop_name}"'}), 400

    try:
        for col, le in label_encoders.items():
            if col in df_input.columns:
                df_input[col] = le.transform(df_input[col])

        prediction = model.predict(df_input)[0]
        return jsonify({"predicted_yield": float(prediction)})

    except Exception as e:
        logging.error(f"Prediction error for crop {crop_name}: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 400

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json(force=True)

    message = data.get("message")
    session_id = data.get("session_id") or str(uuid.uuid4())

    if not message:
        return jsonify({"error": "Empty message"}), 400

    reply = chat_engine(session_id, message)

    return jsonify({
        "reply": reply,
        "session_id": session_id
    })


@app.route("/api/clear", methods=["POST"])
def clear_chat():
    data = request.get_json(force=True)
    session_id = data.get("session_id")

    if session_id:
        clear_context(session_id)

    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
