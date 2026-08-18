# SafeNtrix - Frontend & Backend Integration Guide

This guide explains how to connect the Flutter frontend with the Python ML models backend.

## Project Structure

```
SafeNtrix/
├── Backend/
│   ├── activity_model.pkl         # Activity prediction model
│   ├── emotion_model.pkl          # Emotion prediction model
│   ├── keyword_model.pkl          # Keyword prediction model
│   ├── train_activity.py          # Activity model training script
│   ├── train_emotion.py           # Emotion model training script
│   └── train_keyword.py           # Keyword model training script
├── streamlit_app/                 # Flutter mobile app
│   ├── lib/
│   │   ├── main.dart              # App entry point
│   │   ├── services/
│   │   │   └── api_service.dart   # API communication service (NEW)
│   │   └── screens/
│   │       └── prediction_screen.dart  # AI Prediction screen (UPDATED)
│   └── pubspec.yaml               # Dependencies configuration
├── backend_api.py                 # Flask API server (NEW)
├── test_backend.py                # Backend test suite (NEW)
├── requirements.txt               # Python dependencies (NEW)
└── README.md                      # This file
```

## ML Models Overview

### 1. Activity Model
**Purpose**: Recognizes physical activities from sensor data
- **Input**: Accelerometer and Gyroscope readings
- **Output**: Activity classification (Walking, Running, Standing, Falling, Struggling)
- **Features**:
  - `accelerometer`: Float (0-12+)
  - `gyroscope`: Float (0-8+)

### 2. Emotion Model
**Purpose**: Detects emotional state from audio features
- **Input**: Audio feature extraction (MFCC + Pitch)
- **Output**: Emotion classification (Normal, Fear, Panic, Anxiety)
- **Features**:
  - `mfcc1`: Float (0-1.0)
  - `mfcc2`: Float (0-1.0)
  - `pitch`: Float (100-350 Hz)

### 3. Keyword Model
**Purpose**: Detects emergency keywords or intent
- **Input**: Feature vector from keyword analysis
- **Output**: Classification (Safe, Emergency)

## Setup Instructions

### Step 1: Install Backend Dependencies

```bash
# Navigate to project root
cd "D:\College Final Year Project\SafeNtrix - AI Powered Women Safety System"

# Create Python virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start the Backend API

```bash
# From the project root directory
python backend_api.py
```

Expected output:
```
Starting SafeNtrix Backend API...
Available endpoints:
  GET  /
  POST /api/predict/activity
  POST /api/predict/emotion
  POST /api/predict/keyword
  POST /api/predict/combined
  GET  /api/test

Server running on http://localhost:5000
```

**The backend must be running for the Flutter app to connect!**

### Step 3: Setup Flutter App

```bash
# Navigate to Flutter app directory
cd streamlit_app

# Get dependencies
flutter pub get

# Run on Chrome (or any other target)
flutter run -d chrome
```

## Backend API Endpoints

### 1. Health Check
```
GET /
Response: {"status": "online", "service": "SafeNtrix Backend API", "models": [...]}
```

### 2. Activity Prediction
```
POST /api/predict/activity
Request Body:
{
  "accelerometer": 5.5,
  "gyroscope": 3.0
}

Response:
{
  "activity": "Running",
  "confidence": 0.892,
  "probabilities": {
    "Walking": 0.15,
    "Running": 0.892,
    "Standing": 0.05,
    "Falling": 0.01,
    "Struggling": 0.0
  }
}
```

### 3. Emotion Prediction
```
POST /api/predict/emotion
Request Body:
{
  "mfcc1": 0.65,
  "mfcc2": 0.60,
  "pitch": 200.0
}

Response:
{
  "emotion": "Fear",
  "confidence": 0.756,
  "probabilities": {
    "Normal": 0.1,
    "Fear": 0.756,
    "Panic": 0.05,
    "Anxiety": 0.094
  }
}
```

### 4. Combined Prediction
```
POST /api/predict/combined
Request Body:
{
  "accelerometer": 5.5,
  "gyroscope": 3.0,
  "mfcc1": 0.65,
  "mfcc2": 0.60,
  "pitch": 200.0
}

Response:
{
  "activity": {
    "prediction": "Running",
    "confidence": 0.892
  },
  "emotion": {
    "prediction": "Fear",
    "confidence": 0.756
  },
  "threat_score": 72,
  "risk_level": "HIGH"
}
```

### 5. Model Test
```
GET /api/test
Response: Test predictions with sample data
```

## Testing the Integration

### Method 1: Backend API Test Suite
```bash
# Run comprehensive tests
python test_backend.py
```

This will:
- ✓ Verify backend is running
- ✓ Test activity prediction with sample inputs
- ✓ Test emotion prediction with sample inputs
- ✓ Test combined predictions
- ✓ Verify threat score calculation
- ✓ Test error handling

### Method 2: Manual Testing with cURL

```bash
# Activity prediction
curl -X POST http://localhost:5000/api/predict/activity \
  -H "Content-Type: application/json" \
  -d "{\"accelerometer\": 5.5, \"gyroscope\": 3.0}"

# Emotion prediction
curl -X POST http://localhost:5000/api/predict/emotion \
  -H "Content-Type: application/json" \
  -d "{\"mfcc1\": 0.65, \"mfcc2\": 0.60, \"pitch\": 200}"

# Combined prediction
curl -X POST http://localhost:5000/api/predict/combined \
  -H "Content-Type: application/json" \
  -d "{\"accelerometer\": 5.5, \"gyroscope\": 3.0, \"mfcc1\": 0.65, \"mfcc2\": 0.60, \"pitch\": 200}"
```

### Method 3: Flutter App Testing

1. Start the backend API
2. Run the Flutter app
3. Navigate to "AI" tab (Prediction Screen)
4. You should see:
   - **✓ Live** indicator if backend is connected
   - **◯ Demo** indicator if backend is unavailable (app falls back to demo mode)
5. Tap "Predict Again" to generate new predictions

## Frontend Integration Details

### API Service (`lib/services/api_service.dart`)

The `ApiService` class handles all communication with the backend:

```dart
// Check if backend is available
bool connected = await ApiService.healthCheck();

// Get activity prediction
var result = await ApiService.predictActivity(
  accelerometer: 5.5,
  gyroscope: 3.0,
);

// Get emotion prediction
var result = await ApiService.predictEmotion(
  mfcc1: 0.65,
  mfcc2: 0.60,
  pitch: 200.0,
);

// Get all predictions + threat score
var result = await ApiService.predictCombined(
  accelerometer: 5.5,
  gyroscope: 3.0,
  mfcc1: 0.65,
  mfcc2: 0.60,
  pitch: 200.0,
);
```

### Prediction Screen (`lib/screens/prediction_screen.dart`)

The updated prediction screen:
- ✓ Automatically checks backend connection on startup
- ✓ Calls backend API for real predictions
- ✓ Shows connection status (Live/Demo)
- ✓ Falls back to demo mode if backend is unavailable
- ✓ Displays loading state while fetching predictions
- ✓ Shows error messages if API calls fail

## Threat Score Calculation

The backend calculates a threat score (0-100) based on:

```
Activity Contribution:
- Walking: 10
- Running: 25
- Standing: 20
- Falling: 90
- Struggling: 80

Emotion Contribution:
- Normal: 10
- Fear: 60
- Panic: 90
- Anxiety: 50

Risk Levels:
- LOW: 0-39%
- MEDIUM: 40-69%
- HIGH: 70-100%
```

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# If occupied, kill the process or change the port in backend_api.py
```

### Models Not Loading
```bash
# Verify model files exist in Backend folder
dir Backend\*.pkl

# If missing, run training scripts
python Backend/train_activity.py
python Backend/train_emotion.py
python Backend/train_keyword.py
```

### Flutter App Shows "Demo Mode"
- Backend is not running or not accessible
- Check if backend is running: `http://localhost:5000` in browser
- Check firewall settings
- Verify network connectivity

### CORS Errors
- Already handled by `flask-cors` in backend
- If still issues, check backend logs

## Performance Optimization

1. **Prediction Caching**: Consider caching predictions for identical inputs
2. **Batch Processing**: Send multiple sensor readings at once
3. **Model Optimization**: Convert models to ONNX format for faster inference
4. **Mobile Integration**: Eventually move models to device (TensorFlow Lite)

## Security Considerations

1. Add API authentication (API key, JWT)
2. Input validation and sanitization
3. Rate limiting to prevent abuse
4. HTTPS/TLS for production
5. Secure model storage

## Next Steps

1. ✓ Test backend API with `test_backend.py`
2. ✓ Run Flutter app and verify connection
3. Test with actual sensor data from phone
4. Integrate real audio processing for emotion detection
5. Implement emergency alert system
6. Deploy to production

## Files Created/Modified

**New Files:**
- `backend_api.py` - Flask API server
- `test_backend.py` - Test suite
- `requirements.txt` - Python dependencies
- `streamlit_app/lib/services/api_service.dart` - Flutter API client
- `INTEGRATION_GUIDE.md` - This file

**Modified Files:**
- `streamlit_app/pubspec.yaml` - Added http dependency
- `streamlit_app/lib/screens/prediction_screen.dart` - Added backend integration

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review backend logs
3. Run test suite to diagnose issues
4. Verify network connectivity

---

**Last Updated**: 2024
**Status**: Ready for Testing
