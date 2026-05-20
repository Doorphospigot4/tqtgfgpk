import 'package:flutter/material.dart';

import '../../api/client.dart';

class LearnScreen extends StatefulWidget {
  const LearnScreen({super.key});

  @override
  State<LearnScreen> createState() => _LearnScreenState();
}

class _LearnScreenState extends State<LearnScreen> {
  final api = TideGuardApi();
  late Future<List<dynamic>> _lessons;

  @override
  void initState() {
    super.initState();
    _lessons = api.listLessons().catchError((_) => <dynamic>[]);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Learn')),
      body: FutureBuilder<List<dynamic>>(
        future: _lessons,
        builder: (context, snap) {
          if (snap.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          final lessons = snap.data ?? [];
          if (lessons.isEmpty) {
            return const Center(child: Text('No lessons available offline.'));
          }
          return ListView.separated(
            padding: const EdgeInsets.all(16),
            itemCount: lessons.length,
            separatorBuilder: (_, __) => const SizedBox(height: 8),
            itemBuilder: (_, i) {
              final l = lessons[i] as Map<String, dynamic>;
              return Card(
                child: ListTile(
                  title: Text(l['title'] as String? ?? ''),
                  subtitle: Text('+${l['xp_reward']} XP'),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
