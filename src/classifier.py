"""
analyzing_sighting/classifier.py

This module defines a classifier for UFO sighting messages.
It uses a simple machine learning model to predict whether a sighting message
represents potential alien communication.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from loguru import logger

class SightingClassifier:
    """
    A classifier that predicts whether a UFO sighting message indicates an alien communication.
    """
    def __init__(self):
        """
        Initialize the classifier by training a simple model on synthetic data.
        """
        logger.info("Initializing SightingClassifier and training model...")
        self.model = self._train_model()
        logger.info("Model training complete.")

    def _train_model(self) -> Pipeline:
        """
        Train a machine learning model using synthetic data.
        For demonstration, we create a small dataset with sample messages and labels.
        """
        # Synthetic training data
        training_data = [
            {"msg": "We have detected an alien communication signal", "shape": "circle", "frequency": 42.0, "label": 1},
            {"msg": "Random noise from radar, nothing unusual", "shape": "triangle", "frequency": 12.5, "label": 0},
            {"msg": "Strange pattern of signals, possible alien", "shape": "oval", "frequency": 50.5, "label": 1},
            {"msg": "Meteor spotted in sky, ignition event", "shape": "circle", "frequency": 20.0, "label": 0},
            {"msg": "Signal repeats and shows intelligence", "shape": "triangle", "frequency": 55.0, "label": 1},
            {"msg": "No unusual signals detected, just background noise", "shape": "square", "frequency": 10.0, "label": 0},
        ]
        df = pd.DataFrame(training_data)
        X = df[["msg", "shape", "frequency"]]
        y = df["label"]

        # Create a preprocessing pipeline: TF-IDF for text, One-Hot for shape, passthrough for numeric
        preprocessor = ColumnTransformer(
            transformers=[
                ("text", TfidfVectorizer(), "msg"),
                ("shape", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["shape"]),
            ],
            remainder="passthrough"
        )

        # Create and train a Random Forest classifier pipeline
        model = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=10, random_state=42))
        ])
        logger.info("Training classifier pipeline with synthetic data...")
        model.fit(X, y)
        return model

    def predict(self, sighting: dict) -> int:
        """
        Predict whether the given sighting dictionary indicates an alien communication.
        Returns 1 for yes, 0 for no.
        """
        # Extract features for the model
        data = {
            "msg": [sighting.get("msg", "")],
            "shape": [sighting.get("shape", "")],
            "frequency": [sighting.get("frequency", 0.0)]
        }
        df = pd.DataFrame(data)
        logger.debug(f"Predicting for sighting: {data}")
        prediction = self.model.predict(df)[0]
        logger.info(f"Predicted class for sighting ID {sighting.get('id')} is {prediction}")
        return int(prediction)
