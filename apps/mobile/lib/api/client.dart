import 'dart:convert';
import 'package:http/http.dart' as http;

const String defaultApiUrl = 'http://10.0.2.2:8000';

class TideGuardApi {
  final String baseUrl;
  TideGuardApi({this.baseUrl = defaultApiUrl});

  Uri _u(String path) => Uri.parse('$baseUrl$path');

  Future<List<dynamic>> listLessons() async {
    final r = await http.get(_u('/education/lessons'));
    if (r.statusCode != 200) throw Exception('lessons failed: ${r.statusCode}');
    return jsonDecode(r.body) as List<dynamic>;
  }

  Future<Map<String, dynamic>> me() async {
    final r = await http.get(_u('/me'));
    if (r.statusCode != 200) throw Exception('me failed: ${r.statusCode}');
    return jsonDecode(r.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> cleanupStats() async {
    final r = await http.get(_u('/cleanups/stats'));
    if (r.statusCode != 200) throw Exception('stats failed: ${r.statusCode}');
    return jsonDecode(r.body) as Map<String, dynamic>;
  }
}
