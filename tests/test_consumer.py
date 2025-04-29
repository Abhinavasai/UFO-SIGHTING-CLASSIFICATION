"""
tests/test_consumer.py

Unit tests for the SightingConsumer.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from consumer import SightingConsumer, classified_sightings

def test_parse_message_valid_json():
    body = b'{"id": "test1", "lat": 12.34, "lon": 56.78, "time": "2025-01-01T00:00:00", "frequency": 7.89, "shape": "triangle", "msg": "Test"}'
    parsed = SightingConsumer.parse_message(body)
    assert isinstance(parsed, dict)
    assert parsed["id"] == "test1"
    assert parsed["shape"] == "triangle"
    assert parsed["frequency"] == 7.89

def test_parse_message_invalid_json():
    body = b'not a json'
    parsed = SightingConsumer.parse_message(body)
    assert parsed == {}
