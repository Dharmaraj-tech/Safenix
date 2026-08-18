import 'monitoring_screen.dart';
import 'dart:math';


import 'package:flutter/material.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {

  final random = Random();

  @override
  Widget build(BuildContext context) {

    int battery = 60 + random.nextInt(40);

    return Scaffold(

      appBar: AppBar(
        title: const Text("SafeNtrix"),
        centerTitle: true,
      ),

      body: Padding(

        padding: const EdgeInsets.all(15),

        child: Column(

          children: [

            Row(

              children: [

                Expanded(
                  child: card(
                    Icons.battery_full,
                    "Battery",
                    "$battery%",
                    Colors.green,
                  ),
                ),

                const SizedBox(width: 10),

                Expanded(
                  child: card(
                    Icons.location_on,
                    "GPS",
                    "Connected",
                    Colors.red,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 10),

            Row(

              children: [

                Expanded(
                  child: card(
                    Icons.wifi,
                    "Network",
                    "Online",
                    Colors.blue,
                  ),
                ),

                const SizedBox(width: 10),

                Expanded(
                  child: card(
                    Icons.thermostat,
                    "Temperature",
                    "31°C",
                    Colors.orange,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 30),

            ElevatedButton.icon(

              style: ElevatedButton.styleFrom(
                minimumSize: const Size(double.infinity, 60),
              ),

              onPressed: () {},

              icon: const Icon(Icons.play_arrow),

              label: const Text(
                "Start AI Monitoring",
                style: TextStyle(fontSize: 18),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget card(
      IconData icon,
      String title,
      String value,
      Color color,
      ) {

    return Card(

      elevation: 5,

      child: Padding(

        padding: const EdgeInsets.all(15),

        child: Column(

          children: [

            Icon(
              icon,
              size: 40,
              color: color,
            ),

            const SizedBox(height: 10),

            Text(title),

            const SizedBox(height: 8),

            Text(
              value,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            )
          ],
        ),
      ),
    );
  }
}