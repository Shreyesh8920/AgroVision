# AgroVision (AgriDash)

AgroVision (also referred to as **AgriDash**) is a full‑stack, machine‑learning–driven agricultural decision support system designed to assist farmers and agri‑stakeholders in making **data‑informed farming decisions**. The project integrates **trained ML models**, a **Flask backend**, and a **web‑based frontend**, and is deployed as a live web application.

This repository represents the **final integrated system**, covering model training, backend integration, frontend interaction, and cloud deployment.

---

## 1. Project Overview

AgroVision (AgriDash) is an **integrated, end-to-end agricultural decision support system** that combines **machine learning–based prediction modules** with an **AI-powered advisory chatbot** inside a single project.

The platform is designed to assist farmers and agri-stakeholders through:

* Structured, form-based predictions (crop, fertilizer, yield)
* Conversational guidance via a context-aware agriculture chatbot

All components share a common backend philosophy and are part of the **same deployable system**, not separate or loosely coupled projects.

---

## 2. Core Intelligent Components

AgroVision consists of **two tightly integrated intelligence layers**:

### A. Machine Learning Prediction Models

These models power the structured recommendation and prediction features.

| Module                    | Algorithm                             |
| ------------------------- | ------------------------------------- |
| Crop Recommendation       | Random Forest Classifier              |
| Fertilizer Recommendation | Random Forest Classifier              |
| Yield Prediction          | Gradient Boosting  |

**Evaluation Summary**:

| Task                      | Metric   | Result |
| ------------------------- | -------- | ------ |
| Crop Recommendation       | Accuracy | ~99%   |
| Fertilizer Recommendation | Accuracy | ~96%   |
| Yield Prediction          | R² Score | ~0.91  |

### Training Summary

* Dataset split: **70% training / 15% validation / 15% testing**
* Categorical features encoded using Label Encoders
* Numerical features scaled where required
* Models selected based on validation performance and generalization

### B. AI Advisory Chatbot

The chatbot acts as a **conversational advisory layer** for agriculture-related queries such as crop suitability, soil health, fertilizer usage, and basic weather context.

Key design characteristics:

* Session-based conversation handling (per user)
* Deterministic context trimming to prevent prompt explosion
* Strict control to avoid unintended paid-model usage
* Graceful handling of rate limits and API failures

The chatbot is integrated into the same backend and follows the same reliability-first design philosophy as the ML modules.

## 3. Model Artifacts

Trained models and preprocessing objects are serialized using `pickle` and stored in the repository.

```
models/
├── crop_model.pkl
├── crop_recommendation_pipeline.pkl
├── fertilizer_model.pkl
├── fertilizer_model_pipeline.pkl
├── yield_model.pkl
├── gb_model_rice.pkl
├── gb_model_wheat.pkl
├── gb_model_maize.pkl
├── gb_model_barley.pkl
├── label_encoders_rice.pkl
├── label_encoders_wheat.pkl
├── label_encoders_maize.pkl
├── label_encoders_barley.pkl
```

All models are loaded at runtime and used strictly for inference.

---

## 4. System Architecture (High-Level)

AgroVision follows a **full-stack, user-centric architecture** where the frontend (UI/UX), backend logic, machine learning models, and chatbot work together as a single system.

```
User (Browser)
   ↓
UI / UX Layer (HTML, CSS, JavaScript)
   • Form-based inputs for crop, fertilizer, yield
   • Chat-based interaction for advisory queries
   • Client-side validation & dynamic UI updates
   ↓
Flask Backend (Application & API Layer)
   • Request handling & routing
   • Input validation & preprocessing
   • Chat session management
   ↓
Intelligence Layer
   • ML Models (.pkl) for prediction
   • Chatbot logic for advisory responses
   ↓
Response Formatting
   • Structured results for UI cards
   • Conversational replies for chat UI
```

The UI is not a passive layer; it actively guides user input, validates data, and presents results in an accessible and intuitive manner.

---

## 5. Project Structure (Relevant Files Only)

```
AgroVision/
├── backend/
│   ├── app2.py              # Flask application entry point
│   ├── wsgi.py              # Gunicorn WSGI configuration
│   ├── model.py             # Model loading & prediction logic
│   ├── database.py          # Database utilities
│   ├── requirements.txt     # Python dependencies
│   ├── models/              # Trained ML models (.pkl)
│   ├── services/            # Weather, soil, geocoding APIs
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── README.md
└── .gitignore
```

---

## 6. Frontend (UI/UX) & Backend Design

### Frontend (UI/UX)

The frontend is designed with a strong focus on **usability and clarity for non-technical users**:

* Clean, dashboard-style UI with dedicated pages for:

  * Crop recommendation
  * Fertilizer recommendation
  * Yield prediction
  * Chat-based advisory
* Intuitive form layouts with guided inputs
* Client-side validation to reduce incorrect submissions
* Dynamic result cards for displaying predictions
* Responsive layout for different screen sizes

The UI acts as the primary interaction layer, ensuring users can access complex ML-driven features without technical knowledge.

### Backend

The Flask backend serves as a **single integration layer** connecting UI, ML models, and chatbot logic.

Key responsibilities:

* Handling API requests from the frontend
* Validating and transforming user inputs
* Routing requests to the correct ML model or chatbot logic
* Managing chat sessions and context
* Returning structured responses suitable for UI rendering

---

## 7. Running the Project Locally

### Prerequisites

* Python 3.9 or higher
* pip

### Steps

```bash
git clone https://github.com/Shreyesh8920/AgroVision.git
cd AgroVision/backend
pip install -r requirements.txt
python app2.py
```

Access the application at:

```
http://127.0.0.1:5000
```

---

## 8. Deployment

* Deployed on **Render**
* Production server: **Gunicorn**
* Linux‑compatible dependency setup
* Automatic redeployment on GitHub commits

### Live Application URL

```
https://agridash.onrender.com
```

---

## 9. Challenges Addressed

* Managing multiple ML models in a single production system
* Maintaining preprocessing consistency between training and inference
* Dependency conflicts during Linux‑based deployment
* Correct WSGI configuration for cloud hosting

---

## 10. Limitations

* Model accuracy depends on dataset quality and regional coverage
* Limited number of crops and regions
* Free cloud deployment introduces cold‑start latency

---

## 11. Future Enhancements

* Region‑specific retraining pipelines
* Integration of IoT‑based real‑time soil data
* Multilingual and voice‑based user interface
* Automated periodic model retraining

---

## 12. Contributors

## Contributors

- **Shreyesh Singh** – Machine learning, AI chatbot development, backend intelligence, and deployment. 🔗 [LinkedIn](https://www.linkedin.com/in/shreyesh-singh-836075290/)

- **Shashwat Singh** – UI/UX design, frontend development, backend logic, and system integration. 🔗 [LinkedIn](https://www.linkedin.com/in/shashwat-singh-057a81213/)


---

## 13. License

This project is intended for **educational, research, and personal use**.
