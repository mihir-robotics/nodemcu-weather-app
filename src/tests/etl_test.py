import unittest
import json
import os
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl import validateSensorData, writeToCache, fetchLatest

class TestAppFunctions(unittest.TestCase):
    def setUp(self):
        self.valid_sensor_data = {
            "temp": 25.0,
            "humidity": 60.0
        }
        self.invalid_sensor_data = {
            "temp": 0.0,
            "humidity": 70.0
        }

    def test_validateSensorData_valid_data(self):
        result = validateSensorData(self.valid_sensor_data)
        self.assertTrue(result)

    def test_validateSensorData_invalid_data(self):
        result = validateSensorData(self.invalid_sensor_data)
        self.assertFalse(result)

    @patch('etl.loadToMongo')
    def test_writeToCache_less_than_limit(self, mock_loadToMongo):
        writeToCache(self.valid_sensor_data)
        with open('cache.json', 'r') as json_file:
            data = json.load(json_file)
        self.assertEqual(len(data), 1)
        mock_loadToMongo.assert_not_called()

    @patch('etl.loadToMongo')
    def test_writeToCache_exceeds_limit(self, mock_loadToMongo):
        # Add 21 records to exceed the limit
        for _ in range(101):
            writeToCache(self.valid_sensor_data)
        with open('cache.json', 'r') as json_file:
            data = json.load(json_file)
        self.assertIn(len(data), [0, 1]) # investigate further
        mock_loadToMongo.assert_called_once()

    def test_fetchLatest_no_cache_file(self):
        result = fetchLatest({})
        self.assertEqual(result, {})

    def test_fetchLatest_with_cache_file(self):
        writeToCache(self.valid_sensor_data)
        result = fetchLatest({})
        self.assertEqual(result, self.valid_sensor_data)

    def tearDown(self):
        # Clean up files created during testing, if any
        if os.path.exists('cache.json'):
            os.remove('cache.json')

if __name__ == '__main__':
    unittest.main()
