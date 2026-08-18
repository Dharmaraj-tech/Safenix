"""
Test script for SafeNtrix Backend API and ML Models
Tests all endpoints and validates predictions
"""

import requests
import json
import time
from pathlib import Path

# Configuration
API_URL = "http://localhost:5000"
TEST_TIMEOUT = 5  # seconds

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")

def test_health_check():
    """Test if backend is running"""
    print_header("Health Check")
    
    try:
        response = requests.get(f"{API_URL}/", timeout=TEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Backend API is online")
            print(f"  Service: {data.get('service', 'N/A')}")
            print(f"  Status: {data.get('status', 'N/A')}")
            print(f"  Available models: {', '.join(data.get('models', []))}")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Make sure it's running on http://localhost:5000")
        return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

def test_activity_prediction():
    """Test activity prediction endpoint"""
    print_header("Activity Prediction Test")
    
    test_cases = [
        {"accelerometer": 2.5, "gyroscope": 1.0, "activity": "Walking"},
        {"accelerometer": 6.0, "gyroscope": 3.5, "activity": "Running"},
        {"accelerometer": 0.5, "gyroscope": 0.3, "activity": "Standing"},
        {"accelerometer": 10.0, "gyroscope": 6.0, "activity": "Falling"},
        {"accelerometer": 7.5, "gyroscope": 5.0, "activity": "Struggling"},
    ]
    
    results = []
    
    for test_case in test_cases:
        try:
            payload = {
                "accelerometer": test_case["accelerometer"],
                "gyroscope": test_case["gyroscope"]
            }
            
            response = requests.post(
                f"{API_URL}/api/predict/activity",
                json=payload,
                timeout=TEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data.get('activity', 'Unknown')
                confidence = data.get('confidence', 0)
                
                # Check if prediction matches expected activity
                match = "✓" if prediction == test_case["activity"] else "✗"
                results.append({
                    "expected": test_case["activity"],
                    "predicted": prediction,
                    "confidence": confidence,
                    "match": match == "✓"
                })
                
                print(f"{match} Input: accel={test_case['accelerometer']}, gyro={test_case['gyroscope']}")
                print(f"  Expected: {test_case['activity']}")
                print(f"  Predicted: {prediction} (confidence: {confidence:.3f})")
                
            else:
                print_error(f"Status code {response.status_code} for input {test_case}")
                results.append({"match": False})
                
        except Exception as e:
            print_error(f"Activity prediction failed: {str(e)}")
            results.append({"match": False})
    
    # Summary
    matches = sum(1 for r in results if r.get("match", False))
    print(f"\n{Colors.BOLD}Activity Prediction: {matches}/{len(results)} correct predictions{Colors.RESET}")
    return len(results) > 0

def test_emotion_prediction():
    """Test emotion prediction endpoint"""
    print_header("Emotion Prediction Test")
    
    test_cases = [
        {"mfcc1": 0.25, "mfcc2": 0.30, "pitch": 130, "emotion": "Normal"},
        {"mfcc1": 0.65, "mfcc2": 0.65, "pitch": 210, "emotion": "Fear"},
        {"mfcc1": 0.90, "mfcc2": 0.90, "pitch": 280, "emotion": "Panic"},
        {"mfcc1": 0.55, "mfcc2": 0.55, "pitch": 195, "emotion": "Anxiety"},
    ]
    
    results = []
    
    for test_case in test_cases:
        try:
            payload = {
                "mfcc1": test_case["mfcc1"],
                "mfcc2": test_case["mfcc2"],
                "pitch": test_case["pitch"]
            }
            
            response = requests.post(
                f"{API_URL}/api/predict/emotion",
                json=payload,
                timeout=TEST_TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                prediction = data.get('emotion', 'Unknown')
                confidence = data.get('confidence', 0)
                
                match = "✓" if prediction == test_case["emotion"] else "✗"
                results.append({
                    "expected": test_case["emotion"],
                    "predicted": prediction,
                    "confidence": confidence,
                    "match": match == "✓"
                })
                
                print(f"{match} Input: mfcc1={test_case['mfcc1']}, mfcc2={test_case['mfcc2']}, pitch={test_case['pitch']}")
                print(f"  Expected: {test_case['emotion']}")
                print(f"  Predicted: {prediction} (confidence: {confidence:.3f})")
                
            else:
                print_error(f"Status code {response.status_code} for input {test_case}")
                results.append({"match": False})
                
        except Exception as e:
            print_error(f"Emotion prediction failed: {str(e)}")
            results.append({"match": False})
    
    # Summary
    matches = sum(1 for r in results if r.get("match", False))
    print(f"\n{Colors.BOLD}Emotion Prediction: {matches}/{len(results)} correct predictions{Colors.RESET}")
    return len(results) > 0

def test_combined_prediction():
    """Test combined prediction endpoint"""
    print_header("Combined Prediction Test")
    
    test_data = {
        "accelerometer": 7.5,
        "gyroscope": 4.0,
        "mfcc1": 0.75,
        "mfcc2": 0.70,
        "pitch": 220.0
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/predict/combined",
            json=test_data,
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print_success("Combined prediction successful")
            print(f"\nInput Data:")
            for key, value in test_data.items():
                print(f"  {key}: {value}")
            
            print(f"\nPredictions:")
            
            # Activity
            if 'activity' in data and 'error' not in data['activity']:
                activity = data['activity']
                print(f"  Activity: {activity.get('prediction', 'N/A')} (confidence: {activity.get('confidence', 0):.3f})")
            
            # Emotion
            if 'emotion' in data and 'error' not in data['emotion']:
                emotion = data['emotion']
                print(f"  Emotion: {emotion.get('prediction', 'N/A')} (confidence: {emotion.get('confidence', 0):.3f})")
            
            # Threat Score
            threat = data.get('threat_score', 0)
            risk = data.get('risk_level', 'UNKNOWN')
            print(f"\n  Threat Score: {threat}%")
            print(f"  Risk Level: {risk}")
            
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Combined prediction failed: {str(e)}")
        return False

def test_models_endpoint():
    """Test the models test endpoint"""
    print_header("Models Test Endpoint")
    
    try:
        response = requests.get(
            f"{API_URL}/api/test",
            timeout=TEST_TIMEOUT
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'success':
                print_success("Models test endpoint successful")
                
                print(f"\nTest Results:")
                
                if 'activity' in data:
                    print(f"  Activity: {data['activity'].get('prediction', 'N/A')} (confidence: {data['activity'].get('confidence', 0):.3f})")
                
                if 'emotion' in data:
                    print(f"  Emotion: {data['emotion'].get('prediction', 'N/A')} (confidence: {data['emotion'].get('confidence', 0):.3f})")
                
                if 'threat_score' in data:
                    print(f"  Threat Score: {data['threat_score']}%")
                    print(f"  Risk Level: {data.get('risk_level', 'N/A')}")
                
                return True
            else:
                print_error("Test endpoint returned error status")
                return False
        else:
            print_error(f"Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Models test failed: {str(e)}")
        return False

def test_error_handling():
    """Test error handling for invalid inputs"""
    print_header("Error Handling Tests")
    
    # Test activity prediction with missing fields
    print("Testing activity prediction with missing fields...")
    response = requests.post(
        f"{API_URL}/api/predict/activity",
        json={"accelerometer": 5.0},  # Missing gyroscope
        timeout=TEST_TIMEOUT
    )
    
    if response.status_code == 400:
        print_success("Correctly rejected missing gyroscope field")
    else:
        print_error(f"Expected 400, got {response.status_code}")
    
    # Test emotion prediction with missing fields
    print("\nTesting emotion prediction with missing fields...")
    response = requests.post(
        f"{API_URL}/api/predict/emotion",
        json={"mfcc1": 0.5},  # Missing mfcc2 and pitch
        timeout=TEST_TIMEOUT
    )
    
    if response.status_code == 400:
        print_success("Correctly rejected missing emotion fields")
    else:
        print_error(f"Expected 400, got {response.status_code}")

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║        SafeNtrix Backend API & Models Test Suite       ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    
    print_info(f"Testing API at: {API_URL}")
    print_info(f"Timeout: {TEST_TIMEOUT} seconds")
    
    # Run tests
    tests_passed = 0
    tests_total = 0
    
    # Health check (required for other tests)
    if test_health_check():
        tests_passed += 1
    tests_total += 1
    
    if tests_passed < tests_total:
        print_error("Backend is not running. Please start the backend API first.")
        return
    
    # Run remaining tests
    tests = [
        test_activity_prediction,
        test_emotion_prediction,
        test_combined_prediction,
        test_models_endpoint,
        test_error_handling,
    ]
    
    for test in tests:
        try:
            if test():
                tests_passed += 1
        except Exception as e:
            print_error(f"Test failed with exception: {str(e)}")
        tests_total += 1
    
    # Print summary
    print_header("Test Summary")
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print_success(f"All {tests_total} tests passed!")
    else:
        print_error(f"{tests_total - tests_passed} test(s) failed")

if __name__ == "__main__":
    run_all_tests()
