import 'package:flutter/material.dart';

import 'dashboard_screen.dart';
import 'monitoring_screen.dart';
import 'prediction_screen.dart';
import 'emergency_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {

  int currentIndex = 0;

  final pages = const [
    DashboardScreen(),
    MonitoringScreen(),
    PredictionScreen(),
    EmergencyScreen(),
  ];

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      body: pages[currentIndex],

      bottomNavigationBar: NavigationBar(

        selectedIndex: currentIndex,

        onDestinationSelected: (index){

          setState(() {

            currentIndex = index;

          });

        },

        destinations: const [

          NavigationDestination(
            icon: Icon(Icons.home),
            label: "Home",
          ),

          NavigationDestination(
            icon: Icon(Icons.sensors),
            label: "Monitor",
          ),

          NavigationDestination(
            icon: Icon(Icons.psychology),
            label: "AI",
          ),

          NavigationDestination(
            icon: Icon(Icons.warning),
            label: "SOS",
          ),

        ],
      ),
    );
  }
}