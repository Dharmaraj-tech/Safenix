import 'dart:convert';
import 'package:http/http.dart' as http;

/// API Service for communicating with SafeNtrix backend
class ApiService {
  // Backend API configuration
  static const String baseUrl = "http://localhost:5000";
  static const int timeoutSeconds = 10;

  /// Health check - verify backend is running
  static Future<bool> healthCheck() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: timeoutSeconds));

      return response.statusCode == 200;
    } catch (e) {
      print('Health check failed: $e');
      return false;
    }
  }

  /// Predict activity from accelerometer and gyroscope data
  /// Returns: {"activity": String, "confidence": double, "probabilities": Map}
  static Future<Map<String, dynamic>> predictActivity({
    required double accelerometer,
    required double gyroscope,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/predict/activity'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'accelerometer': accelerometer,
          'gyroscope': gyroscope,
        }),
      ).timeout(const Duration(seconds: timeoutSeconds));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {'error': 'Activity prediction failed: ${response.statusCode}'};
      }
    } catch (e) {
      print('Activity prediction error: $e');
      return {'error': 'Activity prediction error: $e'};
    }
  }

  /// Predict emotion from audio features (MFCC and pitch)
  /// Returns: {"emotion": String, "confidence": double, "probabilities": Map}
  static Future<Map<String, dynamic>> predictEmotion({
    required double mfcc1,
    required double mfcc2,
    required double pitch,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/predict/emotion'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'mfcc1': mfcc1,
          'mfcc2': mfcc2,
          'pitch': pitch,
        }),
      ).timeout(const Duration(seconds: timeoutSeconds));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {'error': 'Emotion prediction failed: ${response.statusCode}'};
      }
    } catch (e) {
      print('Emotion prediction error: $e');
      return {'error': 'Emotion prediction error: $e'};
    }
  }

  /// Predict keyword/intent from audio
  /// Returns: {"keyword": String, "confidence": double}
  static Future<Map<String, dynamic>> predictKeyword({
    required Map<String, dynamic> features,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/predict/keyword'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(features),
      ).timeout(const Duration(seconds: timeoutSeconds));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {'error': 'Keyword prediction failed: ${response.statusCode}'};
      }
    } catch (e) {
      print('Keyword prediction error: $e');
      return {'error': 'Keyword prediction error: $e'};
    }
  }

  /// Combined prediction - get activity, emotion and threat score
  /// Returns all predictions with threat score
  static Future<Map<String, dynamic>> predictCombined({
    required double accelerometer,
    required double gyroscope,
    required double mfcc1,
    required double mfcc2,
    required double pitch,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/predict/combined'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'accelerometer': accelerometer,
          'gyroscope': gyroscope,
          'mfcc1': mfcc1,
          'mfcc2': mfcc2,
          'pitch': pitch,
        }),
      ).timeout(const Duration(seconds: timeoutSeconds));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {'error': 'Combined prediction failed: ${response.statusCode}'};
      }
    } catch (e) {
      print('Combined prediction error: $e');
      return {'error': 'Combined prediction error: $e'};
    }
  }

  /// Test endpoint - run model tests with sample data
  static Future<Map<String, dynamic>> testModels() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/test'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: timeoutSeconds));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {'error': 'Model test failed: ${response.statusCode}'};
      }
    } catch (e) {
      print('Model test error: $e');
      return {'error': 'Model test error: $e'};
    }
  }
}
