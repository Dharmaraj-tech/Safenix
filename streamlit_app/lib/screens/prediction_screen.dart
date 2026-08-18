import 'dart:math';
import 'emergency_screen.dart';
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  State<PredictionScreen> createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {

  final random = Random();

  String activity = "";
  String emotion = "";
  String keyword = "";

  double activityConf = 0;
  double emotionConf = 0;
  double keywordConf = 0;

  int threat = 0;
  
  bool isLoading = false;
  String? errorMessage;
  bool backendConnected = false;

  @override
  void initState() {
    super.initState();
    checkBackendConnection();
  }

  /// Check if backend API is available
  Future<void> checkBackendConnection() async {
    bool connected = await ApiService.healthCheck();
    setState(() {
      backendConnected = connected;
    });
    if (connected) {
      generatePrediction();
    } else {
      setState(() {
        errorMessage = "Backend API not available. Using demo mode.";
      });
      generateDemoPrediction();
    }
  }

  /// Generate prediction using backend API
  Future<void> generatePrediction() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      // Generate random sensor data
      double accelerometer = random.nextDouble() * 12;
      double gyroscope = random.nextDouble() * 8;
      double mfcc1 = random.nextDouble();
      double mfcc2 = random.nextDouble();
      double pitch = 100 + random.nextDouble() * 200;

      // Get predictions from backend
      final result = await ApiService.predictCombined(
        accelerometer: accelerometer,
        gyroscope: gyroscope,
        mfcc1: mfcc1,
        mfcc2: mfcc2,
        pitch: pitch,
      );

      setState(() {
        isLoading = false;

        if (result.containsKey('error')) {
          errorMessage = result['error'];
          generateDemoPrediction();
          backendConnected = false;
        } else {
          // Extract activity prediction
          if (result['activity'] != null &&
              result['activity']['prediction'] != null) {
            activity = result['activity']['prediction'];
            activityConf = (result['activity']['confidence'] ?? 0).toDouble();
          }

          // Extract emotion prediction
          if (result['emotion'] != null &&
              result['emotion']['prediction'] != null) {
            emotion = result['emotion']['prediction'];
            emotionConf = (result['emotion']['confidence'] ?? 0).toDouble();
          }

          // Extract threat score
          threat = (result['threat_score'] ?? 50).toInt();
          
          // For keyword, use safe/emergency based on threat
          keyword = threat > 60 ? "Emergency" : "Safe";
          keywordConf = 0.85;

          backendConnected = true;
        }
      });
    } catch (e) {
      setState(() {
        isLoading = false;
        errorMessage = 'Error: ${e.toString()}';
        backendConnected = false;
      });
      generateDemoPrediction();
    }
  }

  /// Generate demo prediction (when backend is not available)
  void generateDemoPrediction() {
    final activities = ["Standing", "Walking", "Running", "Falling", "Struggling"];
    final emotions = ["Normal", "Fear", "Anxiety", "Panic"];

    activity = activities[random.nextInt(activities.length)];
    emotion = emotions[random.nextInt(emotions.length)];
    keyword = random.nextBool() ? "Emergency" : "Safe";

    activityConf = 0.5 + random.nextDouble() * 0.5;
    emotionConf = 0.5 + random.nextDouble() * 0.5;
    keywordConf = 0.7 + random.nextDouble() * 0.3;

    threat = random.nextInt(101);

    setState(() {});
  }

  Color getColor() {

    if(threat < 40){
      return Colors.green;
    }

    if(threat < 70){
      return Colors.orange;
    }

    return Colors.red;
  }

  String getRisk(){

    if(threat < 40){
      return "LOW RISK";
    }

    if(threat < 70){
      return "MEDIUM RISK";
    }

    return "HIGH RISK";
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("AI Prediction"),
        actions: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Center(
              child: Tooltip(
                message: backendConnected ? "Backend Connected" : "Demo Mode",
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: backendConnected ? Colors.green : Colors.orange,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    backendConnected ? "✓ Live" : "◯ Demo",
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),

      body: isLoading
          ? const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text("Getting predictions from backend..."),
                ],
              ),
            )
          : ListView(

        padding: const EdgeInsets.all(16),

        children: [
          
          // Error message if any
          if (errorMessage != null)
            Card(
              color: Colors.orange.shade100,
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Row(
                  children: [
                    const Icon(Icons.info, color: Colors.orange),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        errorMessage!,
                        style: const TextStyle(
                          color: Colors.orange,
                          fontSize: 12,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

          if (errorMessage != null) const SizedBox(height: 16),

          predictionCard(
              "Activity",
              activity,
              activityConf
          ),

          predictionCard(
              "Emotion",
              emotion,
              emotionConf
          ),

          predictionCard(
              "Keyword",
              keyword,
              keywordConf
          ),

          const SizedBox(height:20),

          Card(

            child: Padding(

              padding: const EdgeInsets.all(20),

              child: Column(

                children: [

                  const Text(
                    "Threat Score",
                    style: TextStyle(
                      fontSize:20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height:20),

                  CircularProgressIndicator(

                    value: threat/100,

                    strokeWidth:12,

                    color:getColor(),

                  ),

                  const SizedBox(height:15),

                  Text(

                    "$threat%",

                    style: const TextStyle(
                      fontSize:30,
                      fontWeight: FontWeight.bold,
                    ),

                  ),

                  const SizedBox(height:10),

                  Text(

                    getRisk(),

                    style: TextStyle(

                      color:getColor(),

                      fontSize:22,

                      fontWeight: FontWeight.bold,

                    ),
                  )

                ],
              ),
            ),
          ),

          const SizedBox(height:20),

          ElevatedButton.icon(
            onPressed: isLoading ? null : generatePrediction,
            icon: const Icon(Icons.refresh),
            label: const Text("Predict Again"),
          ),

          const SizedBox(height: 15),

          ElevatedButton.icon(

            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              minimumSize: const Size(double.infinity, 55),
            ),

            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => const EmergencyScreen(),
                ),
              );
            },

            icon: const Icon(Icons.warning),

            label: const Text("Open Emergency Center"),

          ),
        ],
      ),
    );
  }

  Widget predictionCard(
      String title,
      String value,
      double confidence,
      ){

    return Card(

      margin: const EdgeInsets.only(bottom:15),

      child: Padding(

        padding: const EdgeInsets.all(16),

        child: Column(

          crossAxisAlignment: CrossAxisAlignment.start,

          children: [

            Text(
              title,
              style: const TextStyle(
                fontSize:18,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height:8),

            Text(
              value,
              style: const TextStyle(
                fontSize:22,
              ),
            ),

            const SizedBox(height:10),

            LinearProgressIndicator(
              value: confidence,
            ),

            const SizedBox(height:5),

            Text(
              "${(confidence*100).toStringAsFixed(1)}%",
            )

          ],
        ),
      ),
    );
  }
}