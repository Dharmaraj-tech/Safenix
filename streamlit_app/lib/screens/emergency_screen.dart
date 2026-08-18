import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

class EmergencyScreen extends StatefulWidget {
  const EmergencyScreen({super.key});

  @override
  State<EmergencyScreen> createState() => _EmergencyScreenState();
}

class _EmergencyScreenState extends State<EmergencyScreen> {

  String latitude = "Loading...";
  String longitude = "Loading...";

  @override
  void initState() {
    super.initState();
    getLocation();
  }

  Future<void> getLocation() async {

    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();

    if (!serviceEnabled) {
      return;
    }

    LocationPermission permission =
        await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    Position position = await Geolocator.getCurrentPosition(
      desiredAccuracy: LocationAccuracy.high,
    );

    setState(() {

      latitude = position.latitude.toStringAsFixed(6);

      longitude = position.longitude.toStringAsFixed(6);

    });

  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(

      appBar: AppBar(
        title: const Text("Emergency Response"),
        backgroundColor: Colors.red,
      ),

      body: ListView(

        padding: const EdgeInsets.all(16),

        children: [

          Card(

            color: Colors.red.shade50,

            child: const Padding(

              padding: EdgeInsets.all(20),

              child: Column(

                children: [

                  Icon(
                    Icons.warning,
                    size: 80,
                    color: Colors.red,
                  ),

                  SizedBox(height: 15),

                  Text(
                    "EMERGENCY DETECTED",
                    style: TextStyle(
                      fontSize: 25,
                      fontWeight: FontWeight.bold,
                      color: Colors.red,
                    ),
                  ),

                  SizedBox(height: 10),

                  Text(
                    "Threat Level : HIGH",
                    style: TextStyle(fontSize: 18),
                  )

                ],
              ),
            ),
          ),

          const SizedBox(height:20),

          ElevatedButton.icon(

            onPressed: () {

              ScaffoldMessenger.of(context).showSnackBar(

                const SnackBar(
                  content: Text("SMS Alert Sent"),
                ),

              );

            },

            icon: const Icon(Icons.sms),

            label: const Text("Send SMS Alert"),

            style: ElevatedButton.styleFrom(

              backgroundColor: Colors.orange,

              minimumSize: const Size(double.infinity,55),

            ),

          ),

          const SizedBox(height:15),

          ElevatedButton.icon(

            onPressed: () {

              ScaffoldMessenger.of(context).showSnackBar(

                const SnackBar(
                  content: Text("Calling Guardian..."),
                ),

              );

            },

            icon: const Icon(Icons.call),

            label: const Text("Call Guardian"),

            style: ElevatedButton.styleFrom(

              backgroundColor: Colors.green,

              minimumSize: const Size(double.infinity,55),

            ),

          ),

          const SizedBox(height:15),

          ElevatedButton.icon(

            onPressed: () {

              ScaffoldMessenger.of(context).showSnackBar(

                const SnackBar(
                  content: Text("Audio Recording Started"),
                ),

              );

            },

            icon: const Icon(Icons.mic),

            label: const Text("Record Audio"),

            style: ElevatedButton.styleFrom(

              backgroundColor: Colors.blue,

              minimumSize: const Size(double.infinity,55),

            ),

          ),

          const SizedBox(height:20),

          Card(

            child: Padding(

              padding: const EdgeInsets.all(20),

              child: Column(

                crossAxisAlignment: CrossAxisAlignment.start,

                children: [

                  const Text(

                    "Emergency Details",

                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 22,
                    ),

                  ),

                  const SizedBox(height:15),

                  const Text("User : Shree Varsha"),

                  const Text("Phone : +91 9876543210"),

                  const Text("Guardian : +91 9876500000"),

                  const Text("Threat : 92%"),

                  const SizedBox(height:10),

                  Text(
                    "Latitude : $latitude",
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  Text(
                    "Longitude : $longitude",
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                ],

              ),

            ),

          ),

          const SizedBox(height:20),

          Container(

            height:250,

            decoration: BoxDecoration(

              color: Colors.grey.shade300,

              borderRadius: BorderRadius.circular(15),

            ),

            child: Column(

              mainAxisAlignment: MainAxisAlignment.center,

              children: [

                const Icon(
                  Icons.map,
                  size:80,
                ),

                const SizedBox(height:10),

                const Text(

                  "Google Map",

                  style: TextStyle(
                    fontSize:20,
                    fontWeight: FontWeight.bold,
                  ),

                ),

                const SizedBox(height:10),

                Text(
                  "Latitude : $latitude",
                ),

                Text(
                  "Longitude : $longitude",
                ),

              ],

            ),

          ),

        ],

      ),

    );

  }

}