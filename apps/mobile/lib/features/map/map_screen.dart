import 'package:flutter/material.dart';

class MapScreen extends StatelessWidget {
  const MapScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Forecast map')),
      body: const Center(
        child: Padding(
          padding: EdgeInsets.all(24.0),
          child: Text(
            'Interactive map coming soon.\n\nIn the meantime, the full forecast is available at tideguard.app/map',
            textAlign: TextAlign.center,
          ),
        ),
      ),
    );
  }
}
