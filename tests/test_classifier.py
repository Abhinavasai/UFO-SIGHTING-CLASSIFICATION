"""
tests/test_classifier.py

Unit tests for the SightingClassifier.
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from classifier import SightingClassifier

def test_predict_returns_binary():
    clf = SightingClassifier()
    sample_sighting = {
        "id": "test1",
        "msg": "Test message for aliens",
        "shape": "circle",
        "frequency": 10.0,
        "lat": 0.0,
        "lon": 0.0,
        "time": "2025-01-01T00:00:00"
    }
    prediction = clf.predict(sample_sighting)
    # Prediction should be 0 or 1
    assert prediction in [0, 1], f"Unexpected prediction value: {prediction}"
