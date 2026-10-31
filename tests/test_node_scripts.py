"""Offline tests: python -m unittest discover -s tests -v (repository root)."""
import importlib.util
import json
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main


merge = load('merge_trip_parameters')
coordinates = load('extract_city_coordinates')


class MergeTests(unittest.TestCase):
    def test_supplement_days_keeps_city_and_preferences(self):
        result = merge('', 3, '', '', '大连', 0, '带父母，少走路', '')
        self.assertEqual((result['city'], result['days'], result['preferences']),
                         ('大连', 3, '带父母，少走路'))

    def test_supplement_city_keeps_days(self):
        self.assertEqual(merge('大连', 0, '', '', '', 3, '带父母', '')['days'], 3)

    def test_append_preferences_returns_fields(self):
        result = merge('', 0, '喜欢海景', '', '大连', 3, '少走路', '')
        self.assertEqual(result['preferences'], '少走路；喜欢海景')
        self.assertEqual(result['city'], '大连')

    def test_update_days_and_date(self):
        result = merge('', 2, '', '11月2日', '大连', 3, '', '明天')
        self.assertEqual((result['days'], result['start_date']), (2, '11月2日'))

    def test_invalid_days_does_not_overwrite(self):
        for value in (-1, 1.5, 'unknown', None):
            self.assertEqual(merge('', value, '', '', '大连', 3, '', '')['days'], 3)


class CoordinateTests(unittest.TestCase):
    def test_coordinates_and_local_date(self):
        result = coordinates(json.dumps({'coord': {'lat': 30.2937, 'lon': 120.1614}, 'timezone': 28800}))
        self.assertEqual((result['lat'], result['lon']), ('30.2937', '120.1614'))
        # The date belongs to the API city's offset, not the host machine timezone.
        expected = datetime.now(timezone.utc).astimezone(timezone(timedelta(seconds=28800)))
        self.assertLessEqual(abs((datetime.strptime(result['current_local_date'], '%Y-%m-%d').date()
                                 - expected.date()).days), 1)


if __name__ == '__main__':
    unittest.main()
