"""
SafeNtrix Backend API - Flask Server
Connects ML models with Flutter frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Load models
BASE_DIR = Path(__file__).parent / "Backend"

try:
    activity_model = joblib.load(BASE_DIR / "activity_model.pkl")
    emotion_model = joblib.load(BASE_DIR / "emotion_model.pkl")
    keyword_model = joblib.load(BASE_DIR / "keyword_model.pkl")
    print("✓ All models loaded successfully!")
except Exception as e:
    print(f"✗ Error loading models: {e}")

# Model label mappings
ACTIVITY_LABELS = ["Walking", "Running", "Standing", "Falling", "Struggling"]
EMOTION_LABELS = ["Normal", "Fear", "Panic", "Anxiety"]
KEYWORD_LABELS = ["Safe", "Emergency"]


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "SafeNtrix Backend API",
        "models": ["activity", "emotion", "keyword"]
    }), 200


@app.route('/api/predict/activity', methods=['POST'])
def predict_activity():
    """
    Predict activity from sensor data
    Expected input: {"accelerometer": float, "gyroscope": float}
    """
    try:
        data = request.json
        
        if not data or 'accelerometer' not in data or 'gyroscope' not in data:
            return jsonify({
                "error": "Missing required fields: accelerometer, gyroscope"
            }), 400
        
        accel = float(data['accelerometer'])
        gyro = float(data['gyroscope'])
        
        # Prepare input for model
        features = np.array([[accel, gyro]])
        
        # Get prediction and probabilities
        prediction = activity_model.predict(features)[0]
        probabilities = activity_model.predict_proba(features)[0]
        
        # Find confidence
        confidence = float(np.max(probabilities))
        
        return jsonify({
            "activity": str(prediction),
            "confidence": round(confidence, 3),
            "probabilities": {
                activity: float(prob) 
                for activity, prob in zip(ACTIVITY_LABELS, probabilities)
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/predict/emotion', methods=['POST'])
def predict_emotion():
    """
    Predict emotion from audio features
    Expected input: {"mfcc1": float, "mfcc2": float, "pitch": float}
    """
    try:
        data = request.json
        
        if not data or 'mfcc1' not in data or 'mfcc2' not in data or 'pitch' not in data:
            return jsonify({
                "error": "Missing required fields: mfcc1, mfcc2, pitch"
            }), 400
        
        mfcc1 = float(data['mfcc1'])
        mfcc2 = float(data['mfcc2'])
        pitch = float(data['pitch'])
        
        # Prepare input for model
        features = np.array([[mfcc1, mfcc2, pitch]])
        
        # Get prediction and probabilities
        prediction = emotion_model.predict(features)[0]
        probabilities = emotion_model.predict_proba(features)[0]
        
        # Find confidence
        confidence = float(np.max(probabilities))
        
        return jsonify({
            "emotion": str(prediction),
            "confidence": round(confidence, 3),
            "probabilities": {
                emotion: float(prob) 
                for emotion, prob in zip(EMOTION_LABELS, probabilities)
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/predict/keyword', methods=['POST'])
def predict_keyword():
    """
    Predict keyword/intent from audio text or features
    Expected input: {"feature1": float, "feature2": float, ...}
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                "error": "No data provided"
            }), 400
        
        # For keyword model, we'll extract available features
        # Adjust based on your actual keyword model features
        features_list = []
        for key in sorted(data.keys()):
            if key != 'text':
                features_list.append(float(data[key]))
        
        if not features_list:
            return jsonify({
                "error": "No numeric features provided"
            }), 400
        
        features = np.array([features_list])
        
        # Get prediction and probabilities
        prediction = keyword_model.predict(features)[0]
        probabilities = keyword_model.predict_proba(features)[0]
        
        # Find confidence
        confidence = float(np.max(probabilities))
        
        return jsonify({
            "keyword": str(prediction),
            "confidence": round(confidence, 3),
            "probabilities": {
                keyword: float(prob) 
                for keyword, prob in zip(KEYWORD_LABELS, probabilities)
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/predict/combined', methods=['POST'])
def predict_combined():
    """
    Combined prediction with threat score calculation
    Expected input: {
        "accelerometer": float, 
        "gyroscope": float,
        "mfcc1": float,
        "mfcc2": float,
        "pitch": float,
        "keyword_features": [float, ...]
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        results = {}
        
        # Activity prediction
        if 'accelerometer' in data and 'gyroscope' in data:
            try:
                accel = float(data['accelerometer'])
                gyro = float(data['gyroscope'])
                features = np.array([[accel, gyro]])
                
                pred = activity_model.predict(features)[0]
                probs = activity_model.predict_proba(features)[0]
                conf = float(np.max(probs))
                
                results['activity'] = {
                    "prediction": str(pred),
                    "confidence": round(conf, 3)
                }
            except Exception as e:
                results['activity'] = {"error": str(e)}
        
        # Emotion prediction
        if 'mfcc1' in data and 'mfcc2' in data and 'pitch' in data:
            try:
                mfcc1 = float(data['mfcc1'])
                mfcc2 = float(data['mfcc2'])
                pitch = float(data['pitch'])
                features = np.array([[mfcc1, mfcc2, pitch]])
                
                pred = emotion_model.predict(features)[0]
                probs = emotion_model.predict_proba(features)[0]
                conf = float(np.max(probs))
                
                results['emotion'] = {
                    "prediction": str(pred),
                    "confidence": round(conf, 3)
                }
            except Exception as e:
                results['emotion'] = {"error": str(e)}
        
        # Calculate threat score
        threat_score = calculate_threat_score(results)
        results['threat_score'] = threat_score
        results['risk_level'] = get_risk_level(threat_score)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def calculate_threat_score(predictions):
    """
    Calculate threat score (0-100) based on predictions
    Higher score = higher threat
    """
    score = 50  # Base score
    
    # Activity contribution
    if 'activity' in predictions and 'prediction' in predictions['activity']:
        activity = predictions['activity']['prediction']
        activity_threat_map = {
            "Walking": 10,
            "Running": 25,
            "Standing": 20,
            "Falling": 90,
            "Struggling": 80
        }
        activity_score = activity_threat_map.get(activity, 50)
        conf = predictions['activity'].get('confidence', 0.5)
        score = (score + activity_score * conf) / 2
    
    # Emotion contribution
    if 'emotion' in predictions and 'prediction' in predictions['emotion']:
        emotion = predictions['emotion']['prediction']
        emotion_threat_map = {
            "Normal": 10,
            "Fear": 60,
            "Panic": 90,
            "Anxiety": 50
        }
        emotion_score = emotion_threat_map.get(emotion, 50)
        conf = predictions['emotion'].get('confidence', 0.5)
        score = (score + emotion_score * conf) / 2
    
    return min(100, max(0, int(score)))


def get_risk_level(threat_score):
    """Determine risk level based on threat score"""
    if threat_score < 40:
        return "LOW"
    elif threat_score < 70:
        return "MEDIUM"
    else:
        return "HIGH"


@app.route('/api/test', methods=['GET'])
def test_models():
    """Test all models with sample data"""
    try:
        test_data = {
            "accelerometer": 5.5,
            "gyroscope": 3.0,
            "mfcc1": 0.65,
            "mfcc2": 0.60,
            "pitch": 200.0
        }
        
        # Use combined prediction endpoint
        response = {
            "status": "success",
            "message": "Testing all models with sample data",
            "test_input": test_data
        }
        
        # Activity test
        accel, gyro = test_data['accelerometer'], test_data['gyroscope']
        features = np.array([[accel, gyro]])
        act_pred = activity_model.predict(features)[0]
        act_conf = float(np.max(activity_model.predict_proba(features)[0]))
        response['activity'] = {"prediction": str(act_pred), "confidence": round(act_conf, 3)}
        
        # Emotion test
        mfcc1, mfcc2, pitch = test_data['mfcc1'], test_data['mfcc2'], test_data['pitch']
        features = np.array([[mfcc1, mfcc2, pitch]])
        emo_pred = emotion_model.predict(features)[0]
        emo_conf = float(np.max(emotion_model.predict_proba(features)[0]))
        response['emotion'] = {"prediction": str(emo_pred), "confidence": round(emo_conf, 3)}
        
        # Calculate threat
        threat = calculate_threat_score({
            'activity': {'prediction': str(act_pred), 'confidence': act_conf},
            'emotion': {'prediction': str(emo_pred), 'confidence': emo_conf}
        })
        response['threat_score'] = threat
        response['risk_level'] = get_risk_level(threat)
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting SafeNtrix Backend API...")
    print("Available endpoints:")
    print("  GET  /")
    print("  POST /api/predict/activity")
    print("  POST /api/predict/emotion")
    print("  POST /api/predict/keyword")
    print("  POST /api/predict/combined")
    print("  GET  /api/test")
    print("\nServer running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
