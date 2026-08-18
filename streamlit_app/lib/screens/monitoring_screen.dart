import 'dart:math';
import 'prediction_screen.dart';
import 'package:flutter/material.dart';

class MonitoringScreen extends StatefulWidget {
  const MonitoringScreen({super.key});

  @override
  State<MonitoringScreen> createState() => _MonitoringScreenState();
}

class _MonitoringScreenState extends State<MonitoringScreen> {

  final Random random = Random();

  bool monitoring = false;

  late double accelerometer;
  late double gyroscope;
  late double noise;
  late double pitch;
  late double mfcc1;
  late double mfcc2;

  @override
  void initState() {
    super.initState();
    generateSensorData();
  }

  void generateSensorData() {
    accelerometer = random.nextDouble() * 10;
    gyroscope = random.nextDouble() * 8;
    noise = 20 + random.nextDouble() * 70;
    pitch = 100 + random.nextDouble() * 220;
    mfcc1 = random.nextDouble();
    mfcc2 = random.nextDouble();
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("AI Monitoring"),
        centerTitle: true,
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: ListView(

          children: [

            SwitchListTile(
              title: const Text("Monitoring"),
              subtitle: const Text("Enable AI Monitoring"),
              value: monitoring,
              onChanged: (value) {
                setState(() {
                  monitoring = value;
                });
              },
            ),

            const SizedBox(height: 20),

            sensorCard(
                Icons.speed,
                "Accelerometer",
                accelerometer.toStringAsFixed(2)
            ),

            sensorCard(
                Icons.rotate_right,
                "Gyroscope",
                gyroscope.toStringAsFixed(2)
            ),

            sensorCard(
                Icons.graphic_eq,
                "Noise",
                "${noise.toStringAsFixed(1)} dB"
            ),

            sensorCard(
                Icons.mic,
                "Pitch",
                pitch.toStringAsFixed(1)
            ),

            sensorCard(
                Icons.analytics,
                "MFCC-1",
                mfcc1.toStringAsFixed(3)
            ),

            sensorCard(
                Icons.analytics,
                "MFCC-2",
                mfcc2.toStringAsFixed(3)
            ),

            const SizedBox(height: 25),

            ElevatedButton.icon(

              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const MonitoringScreen(),
                  ),
                );
              },

              icon: const Icon(Icons.refresh),

              label: const Text("Refresh Sensor Data"),

              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 55),
              ),
            ),

            const SizedBox(height: 15),

            ElevatedButton.icon(

              onPressed: monitoring
    ? () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => const PredictionScreen(),
          ),
        );
      }
    : null,

              icon: const Icon(Icons.play_arrow),

              label: const Text("Start Prediction"),

              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 55),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget sensorCard(
      IconData icon,
      String title,
      String value,
      ) {

    return Card(

      margin: const EdgeInsets.only(bottom: 12),

      elevation: 3,

      child: ListTile(

        leading: CircleAvatar(
          child: Icon(icon),
        ),

        title: Text(title),

        trailing: Text(
          value,
          style: const TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 18,
          ),
        ),
      ),
    );
  }
}