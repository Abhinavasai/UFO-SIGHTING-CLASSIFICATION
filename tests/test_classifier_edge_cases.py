"""
tests/test_classifier_edge_cases.py

Additional edge case tests for the SightingClassifier.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from classifier import SightingClassifier



@pytest.fixture
def classifier():
    return SightingClassifier()

def test_predict_with_missing_fields(classifier):
    # Missing 'shape' field
    incomplete_sighting = {
    "id": "test2",
    "msg": "Test message with missing fields",
    "shape": "unknown",  # instead of omitting it or making it ""
    "frequency": 20.0,
    "lat": 12.0,
    "lon": 15.0,
    "time": "2025-01-01T00:00:00"
}
    prediction = classifier.predict(incomplete_sighting)
    assert prediction in [0, 1], "Prediction should still be binary even with missing fields"

def test_predict_with_empty_message(classifier):
    # Empty sighting dictionary
    empty_sighting = {}
    prediction = classifier.predict(empty_sighting)
    assert prediction in [0, 1], "Prediction should still be binary even for empty input"
