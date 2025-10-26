from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Cache dictionaries for lazy loading
fertilizer_cache = {}
crop_rec_cache = {}
yield_model_cache = {}
yield_label_encoder_cache = {}

# -------- Utility Load Functions --------
def load_fertilizer_model():
    if not fertilizer_cache:
        with open('fertilizer_model_pipeline.pkl', 'rb') as f:
            objs = pickle.load(f)
            fertilizer_cache['model'] = objs['model']
            fertilizer_cache['scaler'] = objs['scaler']
            fertilizer_cache['le_crop'] = objs['le_crop']
            fertilizer_cache['le_soil'] = objs['le_soil']
            fertilizer_cache['le_fert'] = objs['le_fert']
    return fertilizer_cache

def load_crop_rec_model():
    if not crop_rec_cache:
        with open('crop_recommendation_pipeline.pkl', 'rb') as f:
            objs = pickle.load(f)
            crop_rec_cache['model'] = objs['model']
            crop_rec_cache['scaler'] = objs['scaler']
            crop_rec_cache['label_encoder'] = objs['label_encoder']
    return crop_rec_cache

def load_yield_model_and_encoders(crop_name):
    if crop_name not in yield_model_cache:
        # Load model
        model_filename = f'gb_model_{crop_name}.pkl'
        le_filename = f'label_encoders_{crop_name}.pkl'
        try:
            with open(model_filename, 'rb') as f:
                yield_model_cache[crop_name] = pickle.load(f)
            with open(le_filename, 'rb') as f:
                yield_label_encoder_cache[crop_name] = pickle.load(f)
        except FileNotFoundError:
            return None, None
    return yield_model_cache[crop_name], yield_label_encoder_cache[crop_name]

# -------- Routes --------

@app.route('/recommend_fertilizer', methods=['POST'])
def recommend_fertilizer():
    data = request.json
    model_objs = load_fertilizer_model()
    df_input = pd.DataFrame([data])
    df_input['Crop_le'] = model_objs['le_crop'].transform(df_input['Crop'])
    df_input['Soil_le'] = model_objs['le_soil'].transform(df_input['Soil'])
    numeric_cols = ['Nitrogen', 'Phosphorous', 'Potassium', 'PH', 'Temperature',
                    'Moisture', 'Rainfall', 'Carbon']
    df_input[numeric_cols] = model_objs['scaler'].transform(df_input[numeric_cols])
    features = numeric_cols + ['Crop_le', 'Soil_le']
    X = df_input[features]
    pred_encoded = model_objs['model'].predict(X)[0]
    pred_fert = model_objs['le_fert'].inverse_transform([pred_encoded])[0]
    return jsonify({'recommended_fertilizer': pred_fert})

@app.route('/recommend_crop', methods=['POST'])
def recommend_crop():
    data = request.json
    model_objs = load_crop_rec_model()
    df_input = pd.DataFrame([data])
    df_scaled = model_objs['scaler'].transform(df_input)
    pred_encoded = model_objs['model'].predict(df_scaled)[0]
    predicted_crop = model_objs['label_encoder'].inverse_transform([pred_encoded])[0]
    return jsonify({'recommended_crop': predicted_crop})

@app.route('/predict_yield', methods=['POST'])
def predict_yield():
    data = request.json
    if not data or 'crop_name' not in data:
        return jsonify({'error': 'Input JSON must include "crop_name" and other features'}), 400

    crop_name = data['crop_name'].lower()
    input_features = {k: v for k, v in data.items() if k != 'crop_name'}
    df_input = pd.DataFrame({k: [v] if not isinstance(v, list) else v for k, v in input_features.items()})

    model, label_encoders = load_yield_model_and_encoders(crop_name)
    if model is None or label_encoders is None:
        return jsonify({'error': f'No model found for crop "{crop_name}"'}), 400

    for col, le in label_encoders.items():
        if col in df_input.columns:
            df_input[col] = le.transform(df_input[col])

    prediction = model.predict(df_input)[0]
    return jsonify({'predicted_yield': float(prediction)})

# ------- Main -------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
