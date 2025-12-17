# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from services.weather_api import get_weather
# from services.geocoding import geocode
# from services.soil_api import get_soil
# from model import db, FarmData
# import pickle
# import pandas as pd
# import logging
# from pathlib import Path

# app = Flask(__name__)
# CORS(app)

# # ---------------- Database Setup ----------------
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmdata.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)

# with app.app_context():
#     db.create_all()

# # ---------------- ML Model Caches ----------------
# fertilizer_cache = {}
# crop_cache = {}
# yield_model_cache = {}
# yield_label_encoder_cache = {}

# # -------- Utility Load Functions --------

# def load_fertilizer_model():
#     if not fertilizer_cache:
#         model_path = Path(__file__).parent / 'fertilizer_model_pipeline.pkl'

#         with model_path.open('rb') as f:
#             objs = pickle.load(f)

#         fertilizer_cache['model'] = objs['model']
#         fertilizer_cache['scaler'] = objs['scaler']
#         fertilizer_cache['le_crop'] = objs['le_crop']
#         fertilizer_cache['le_soil'] = objs['le_soil']
#         fertilizer_cache['le_fert'] = objs['le_fert']

#     return fertilizer_cache

# from pathlib import Path
# import pickle

# def load_crop_rec_model():
#     if not crop_cache:
#         base_dir = Path(__file__).resolve().parent
#         model_path = base_dir / 'crop_recommendation_pipeline.pkl'

#         with model_path.open('rb') as f:
#             objs = pickle.load(f)
#             crop_cache['model'] = objs['model']
#             crop_cache['scaler'] = objs['scaler']
#             crop_cache['label_encoder'] = objs['label_encoder']

#     return crop_cache


# from pathlib import Path
# import pickle
# import logging

# def load_yield_model_and_encoders(crop_name):
#     base_dir = Path(__file__).resolve().parent  # backend/
#     crop_name = crop_name.lower().strip()

#     model_path = base_dir / f"gb_model_{crop_name}.pkl"
#     encoder_path = base_dir / f"label_encoders_{crop_name}.pkl"

#     if not model_path.exists() or not encoder_path.exists():
#         logging.error(f"No model or encoders found for crop: {crop_name}")
#         return None, None

#     with model_path.open("rb") as f:
#         model = pickle.load(f)

#     with encoder_path.open("rb") as f:
#         label_encoders = pickle.load(f)

#     return model, label_encoders


# # ---------------- Routes: Basic ----------------

# @app.route("/")
# def home():
#     return {"msg": "Backend Running with ML Integration"}

# @app.route("/weather")
# def weather():
#     lat = request.args.get("lat")
#     lon = request.args.get("lon")
#     if not lat or not lon:
#         return jsonify({"error": "lat and lon are required"}), 400
#     data = get_weather(lat, lon)
#     return jsonify(data)

# @app.route("/geocode")
# def geocode_route():
#     location = request.args.get("location")
#     if not location:
#         return jsonify({"error": "location is required"}), 400
#     lat, lon, place = geocode(location)
#     return jsonify({
#         "location": location,
#         "lat": lat,
#         "lon": lon,
#         "district": place.get("district"),
#         "state": place.get("state")
#     })

# @app.route("/soil")
# def soil_route():
#     lat = request.args.get("lat")
#     lon = request.args.get("lon")
#     if not lat or not lon:
#         return jsonify({"error": "lat and lon are required"}), 400
#     data = get_soil(lat, lon)
#     return jsonify(data)

# @app.route("/store", methods=["POST"])
# def store():
#     data = request.json
#     farm_data = FarmData(
#         lat=data.get("lat"),
#         lon=data.get("lon"),
#         state=data.get("state"),
#         district=data.get("district"),
#         temperature=data.get("temperature"),
#         humidity=data.get("humidity"),
#         rainfall=data.get("rainfall"),
#         soil_moisture=data.get("soil_moisture"),
#         soil_temperature=data.get("soil_temperature")
#     )
#     db.session.add(farm_data)
#     db.session.commit()
#     return jsonify({"msg": "Data stored successfully", "id": farm_data.id})

# @app.route("/fetch", methods=["GET"])
# def fetch():
#     state = request.args.get("state")
#     district = request.args.get("district")
#     query = FarmData.query
#     if state:
#         query = query.filter(FarmData.state == state)
#     if district:
#         query = query.filter(FarmData.district == district)
#     records = query.all()
#     return jsonify([record.to_dict() for record in records])

# @app.route("/collect", methods=["GET"])
# def collect():
#     location = request.args.get("location")
#     lat = request.args.get("lat")
#     lon = request.args.get("lon")

#     if location:
#         lat, lon, place = geocode(location)
#     elif lat is not None and lon is not None:
#         try:
#             lat = float(lat)
#             lon = float(lon)
#             place = {}
#         except ValueError:
#             return jsonify({"error": "lat and lon must be numeric if location is not provided"}), 400
#     else:
#         return jsonify({"error": "Either location or lat and lon are required"}), 400

#     location_name = place.get("location_name") or place.get("city") or place.get("district") or place.get("state") or "Unknown Location"
#     state = place.get("state")
#     district = place.get("district")

#     weather_data = get_weather(lat, lon)
#     temperature = weather_data.get("temperature")
#     humidity = weather_data.get("humidity")
#     rainfall = weather_data.get("rainfall")
#     wind_speed = weather_data.get("wind_speed")
#     uv_index = weather_data.get("uv_index")
#     sunrise = weather_data.get("sunrise")
#     sunset = weather_data.get("sunset")

#     soil_data = get_soil(lat, lon)
#     soil_moisture = soil_data.get("avg_soil_moisture")
#     soil_temperature = soil_data.get("avg_soil_temperature")

#     farm_data = FarmData(
#         lat=lat,
#         lon=lon,
#         state=state,
#         district=district,
#         temperature=temperature,
#         humidity=humidity,
#         rainfall=rainfall,
#         soil_moisture=soil_moisture,
#         soil_temperature=soil_temperature
#     )

#     db.session.add(farm_data)
#     db.session.commit()

#     return jsonify({
#         "location": location_name,
#         "lat": lat,
#         "lon": lon,
#         "state": state,
#         "district": district,
#         "temperature": temperature,
#         "humidity": humidity,
#         "rainfall": rainfall,
#         "soil_moisture": soil_moisture,
#         "soil_temperature": soil_temperature,
#         "wind_speed": wind_speed,
#         "uv_index": uv_index,
#         "sunrise": sunrise,
#         "sunset": sunset,
#         "msg": "Data stored successfully",
#         "id": farm_data.id
#     })

# # ---------------- Routes: ML Integration ----------------

# @app.route('/recommend_fertilizer', methods=['POST'])
# def recommend_fertilizer():
#     data = request.json
#     model_objs = load_fertilizer_model()
#     print("FERTILIZER INPUT FROM UI:", request.json)

#     try:
#         # ---------- REQUIRED FIELDS ----------
#         required_fields = [
#             'Nitrogen', 'Phosphorous', 'Potassium', 'PH',
#             'Temperature', 'Moisture', 'Rainfall', 'Carbon',
#             'Crop', 'Soil'
#         ]

#         missing = [f for f in required_fields if f not in data]
#         if missing:
#             return jsonify({
#                 'error': f'Missing required fields: {missing}'
#             }), 400

#         # ---------- DATAFRAME ----------
#         df_input = pd.DataFrame([data])

#         # ---------- LABEL ENCODING (SAFE) ----------
#         if df_input.at[0, 'Crop'] not in model_objs['le_crop'].classes_:
#             return jsonify({'error': 'Unsupported crop value'}), 400

#         if df_input.at[0, 'Soil'] not in model_objs['le_soil'].classes_:
#             return jsonify({'error': 'Unsupported soil value'}), 400

#         df_input['Crop_le'] = model_objs['le_crop'].transform(df_input['Crop'])
#         df_input['Soil_le'] = model_objs['le_soil'].transform(df_input['Soil'])

#         # ---------- NUMERIC SCALING ----------
#         numeric_cols = [
#             'Nitrogen', 'Phosphorous', 'Potassium', 'PH',
#             'Temperature', 'Moisture', 'Rainfall', 'Carbon'
#         ]

#         df_input[numeric_cols] = model_objs['scaler'].transform(
#             df_input[numeric_cols]
#         )

#         # ---------- FINAL FEATURE ORDER ----------
#         feature_order = numeric_cols + ['Crop_le', 'Soil_le']
#         X = df_input[feature_order]

#         # ---------- PREDICTION ----------
#         pred_encoded = model_objs['model'].predict(X)[0]
#         pred_fert = model_objs['le_fert'].inverse_transform([pred_encoded])[0]

#         return jsonify({'recommended_fertilizer': pred_fert})

#     except Exception as e:
#         return jsonify({
#             'error': f'Prediction failed: {str(e)}'
#         }), 400


# @app.route('/recommend_crop', methods=['POST'])
# def recommend_crop():
#     data = request.json
#     print("CROP INPUT FROM UI:", data)   # 👈 ADD THIS

#     model_objs = load_crop_rec_model()
#     try:
#         df_input = pd.DataFrame([data])
#         print("DF INPUT:", df_input)     # 👈 ADD THIS

#         df_scaled = model_objs['scaler'].transform(df_input)
#         pred_encoded = model_objs['model'].predict(df_scaled)[0]
#         predicted_crop = model_objs['label_encoder'].inverse_transform([pred_encoded])[0]

#         print("PREDICTED CROP:", predicted_crop)  # 👈 ADD THIS
#         return jsonify({'recommended_crop': predicted_crop})

#     except Exception as e:
#         print("CROP PREDICTION ERROR:", str(e))   # 👈 ADD THIS
#         return jsonify({'error': f'Prediction failed: {str(e)}'}), 400


# @app.route('/predict_yield', methods=['POST'])
# def predict_yield():
#     data = request.json
#     print("YIELD_PRED INPUT FROM UI:", request.json)
#     if not data or 'crop_name' not in data:
#         return jsonify({'error': 'Input JSON must include "crop_name" and other features'}), 400
#     crop_name = data['crop_name'].lower()
#     input_features = {k: v for k, v in data.items() if k != 'crop_name'}

#     # Convert 'yes'/'no' strings to boolean True/False for Fertilizer_Used and Irrigation_Used
#     for col in ['Fertilizer_Used', 'Irrigation_Used']:
#         if col in input_features:
#             val = input_features[col]
#             if isinstance(val, list):
#                 raw_val = val[0] if val else None
#                 if isinstance(raw_val, str):
#                     input_features[col][0] = raw_val.strip().lower() == 'Yes'
#             elif isinstance(val, str):
#                 input_features[col] = val.strip().lower() == 'Yes'

#     df_input = pd.DataFrame({k: [v] if not isinstance(v, list) else v for k, v in input_features.items()})

#     model, label_encoders = load_yield_model_and_encoders(crop_name)
#     if model is None or label_encoders is None:
#         logging.error(f"No model found for crop: {crop_name}")
#         return jsonify({'error': f'No model found for crop "{crop_name}"'}), 400
#     try:
#         for col, le in label_encoders.items():
#             if col in df_input.columns:
#                 df_input[col] = le.transform(df_input[col])
#         prediction = model.predict(df_input)[0]
#         return jsonify({'predicted_yield': float(prediction)})
#     except Exception as e:
#         logging.error(f"Prediction error for crop {crop_name}: {str(e)}")
#         return jsonify({'error': f'Prediction failed: {str(e)}'}), 400

# # ---------------- Main ----------------

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5100)

##from here ##########################################################

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import pickle
import logging
import pandas as pd
import numpy as np

# ---- Services ----
from services.weather_api import get_weather
from services.geocoding import geocode
from services.soil_api import get_soil

# --------------------------------------------------
# App & DB setup
# --------------------------------------------------

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmdata.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"

# --------------------------------------------------
# Caches
# --------------------------------------------------

crop_cache = {}
fertilizer_cache = {}
yield_model_cache = {}

# --------------------------------------------------
# DB Model
# --------------------------------------------------

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

# --------------------------------------------------
# Frontend Routes
# --------------------------------------------------

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

# --------------------------------------------------
# Weather / Soil Collection
# --------------------------------------------------

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

    # 🔥 FIX: ensure soil_type is always a string
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

# --------------------------------------------------
# Crop Recommendation
# --------------------------------------------------

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

# --------------------------------------------------
# Fertilizer Recommendation
# --------------------------------------------------

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

        # ---------- LABEL ENCODING ----------
        if df_input.at[0, 'Crop'] not in model_objs['le_crop'].classes_:
            return jsonify({'error': 'Unsupported crop value'}), 400

        if df_input.at[0, 'Soil'] not in model_objs['le_soil'].classes_:
            return jsonify({'error': 'Unsupported soil value'}), 400

        df_input['Crop_le'] = model_objs['le_crop'].transform(df_input['Crop'])
        df_input['Soil_le'] = model_objs['le_soil'].transform(df_input['Soil'])

        # ---------- NUMERIC SCALING ----------
        numeric_cols = [
            'Nitrogen', 'Phosphorous', 'Potassium', 'PH',
            'Temperature', 'Moisture', 'Rainfall', 'Carbon'
        ]

        df_input[numeric_cols] = model_objs['scaler'].transform(
            df_input[numeric_cols]
        )

        # ---------- FINAL FEATURE ORDER ----------
        feature_order = numeric_cols + ['Crop_le', 'Soil_le']
        X = df_input[feature_order]

        # ---------- PREDICTION ----------
        pred_encoded = model_objs['model'].predict(X)[0]
        pred_fert = model_objs['le_fert'].inverse_transform([pred_encoded])[0]

        return jsonify({'recommended_fertilizer': pred_fert})

    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 400


# --------------------------------------------------
# Yield Prediction
# --------------------------------------------------

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

    # Remove crop_name from features
    input_features = {k: v for k, v in data.items() if k != "crop_name"}

    # Convert Yes/No strings to boolean (safety)
    for col in ["Fertilizer_Used", "Irrigation_Used"]:
        if col in input_features:
            val = input_features[col]
            if isinstance(val, list):
                raw_val = val[0] if val else None
                if isinstance(raw_val, str):
                    input_features[col][0] = raw_val.strip().lower() == "true"
            elif isinstance(val, str):
                input_features[col] = val.strip().lower() == "true"

    # Build DataFrame
    df_input = pd.DataFrame({
        k: v if isinstance(v, list) else [v]
        for k, v in input_features.items()
    })

    model, label_encoders = load_yield_model_and_encoders(crop_name)
    if model is None or label_encoders is None:
        logging.error(f"No model found for crop: {crop_name}")
        return jsonify({"error": f'No model found for crop "{crop_name}"'}), 400

    try:
        # 🔥 APPLY ENCODERS SAFELY (THIS IS THE KEY FIX)
        for col, le in label_encoders.items():
            if col in df_input.columns:
                df_input[col] = le.transform(df_input[col])

        prediction = model.predict(df_input)[0]
        return jsonify({"predicted_yield": float(prediction)})

    except Exception as e:
        logging.error(f"Prediction error for crop {crop_name}: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 400



# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)
