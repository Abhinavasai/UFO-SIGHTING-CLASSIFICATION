"""
analyzing_sighting/dashboard.py

Streamlit dashboard for real-time visualization of UFO sighting classifications.
"""

import threading
import pandas as pd
import streamlit as st
from loguru import logger
from consumer import SightingConsumer, classified_sightings
from classifier import SightingClassifier

# Ensure logging from Loguru appears in Streamlit logs
logger.add(lambda msg: st.write(msg, end=""))

st.set_page_config(page_title="UFO Sightings Dashboard", layout="wide")
st.title("UFO Sightings Dashboard")

# Initialize classifier and consumer thread on first load
if 'consumer_started' not in st.session_state:
    st.session_state['consumer_started'] = True
    classifier = SightingClassifier()
    try:
        consumer = SightingConsumer(classifier)
        thread = threading.Thread(target=consumer.start_consuming, daemon=True)
        thread.start()
        logger.info("Started RabbitMQ consumer thread.")
    except Exception as e:
        logger.error(f"Failed to start consumer: {e}")

# Display metrics and data if any sightings have been classified
if classified_sightings:
    df = pd.DataFrame(classified_sightings)
    st.subheader("Classified Sightings Data")
    st.dataframe(df)
    # Show locations on map if latitude and longitude available
    if 'lat' in df.columns and 'lon' in df.columns:
        try:
            st.map(df)
        except Exception as e:
            logger.error(f"Error showing map: {e}")

    # Show distribution of predictions
    st.subheader("Prediction Distribution")
    pred_counts = df['prediction'].value_counts().rename({0: 'Non-alien', 1: 'Alien'})
    st.bar_chart(pred_counts)

    # Show distribution of shapes
    st.subheader("Shapes Observed")
    shape_counts = df['shape'].value_counts()
    st.bar_chart(shape_counts)
else:
    st.info("Waiting for UFO sighting messages...")
