import 'dart:io';

import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:image_picker/image_picker.dart';

class ReportScreen extends StatefulWidget {
  const ReportScreen({super.key});

  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  File? _photo;
  Position? _position;
  int _severity = 3;
  String _debrisType = 'plastic_bottle';

  Future<void> _pick() async {
    final picked = await ImagePicker().pickImage(source: ImageSource.camera, imageQuality: 80);
    if (picked != null) setState(() => _photo = File(picked.path));
    final pos = await Geolocator.getCurrentPosition();
    setState(() => _position = pos);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Report debris')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          ElevatedButton.icon(
            onPressed: _pick,
            icon: const Icon(Icons.camera_alt),
            label: const Text('Take photo + capture GPS'),
          ),
          const SizedBox(height: 12),
          if (_photo != null) Image.file(_photo!, height: 200, fit: BoxFit.cover),
          if (_position != null) Text('Location: ${_position!.latitude.toStringAsFixed(4)}, ${_position!.longitude.toStringAsFixed(4)}'),
          const SizedBox(height: 20),
          Text('Severity: $_severity'),
          Slider(
            value: _severity.toDouble(),
            min: 1,
            max: 5,
            divisions: 4,
            onChanged: (v) => setState(() => _severity = v.toInt()),
          ),
          DropdownButton<String>(
            value: _debrisType,
            isExpanded: true,
            items: const [
              DropdownMenuItem(value: 'plastic_bottle', child: Text('Plastic bottle')),
              DropdownMenuItem(value: 'fishing_net', child: Text('Fishing net')),
              DropdownMenuItem(value: 'foam', child: Text('Foam / polystyrene')),
              DropdownMenuItem(value: 'mixed', child: Text('Mixed plastic')),
            ],
            onChanged: (v) => setState(() => _debrisType = v ?? 'plastic_bottle'),
          ),
          const SizedBox(height: 20),
          FilledButton(
            onPressed: _photo == null || _position == null ? null : () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Report submitted (stub — wire to /reports endpoint)')),
              );
            },
            child: const Text('Submit report'),
          ),
        ],
      ),
    );
  }
}
