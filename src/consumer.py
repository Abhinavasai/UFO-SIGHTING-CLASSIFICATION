"""
analyzing_sighting/consumer.py

This module defines a RabbitMQ consumer that listens for UFO sighting messages
and uses the classifier to label them.
"""

import json
import os
import pika
from loguru import logger
from classifier import SightingClassifier

# Shared list for incoming classified messages (used by the dashboard)
classified_sightings = []

class SightingConsumer:
    """
    Connects to RabbitMQ, subscribes to the 'ufo' exchange, and processes messages.
    """
    def __init__(self, classifier: SightingClassifier, host: str = None, port: int = None, user: str = None, password: str = None):
        # RabbitMQ connection parameters
        self.host = host or os.getenv("RABBITMQ_HOST", "localhost")
        self.port = port or int(os.getenv("RABBITMQ_PORT", "5672"))
        self.user = user or os.getenv("RABBITMQ_USER", "guest")
        self.password = password or os.getenv("RABBITMQ_PASS", "guest")
        self.exchange = "ufo"
        self.classifier = classifier

        logger.info(f"Setting up RabbitMQ connection to {self.host}:{self.port} with user {self.user}")
        credentials = pika.PlainCredentials(self.user, self.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
        )
        self.channel = self.connection.channel()

        # Declare exchange and a temporary queue
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='fanout', durable=True)
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue_name)
        logger.info(f"Subscribed to exchange '{self.exchange}', queue '{self.queue_name}'")

    @staticmethod
    def parse_message(body: bytes) -> dict:
        """
        Parse the RabbitMQ message body (bytes) into a JSON dictionary.
        """
        try:
            data = json.loads(body.decode('utf-8'))
            logger.debug(f"Parsed message: {data}")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return {}

    def _on_message(self, ch, method, properties, body):
        """
        Callback for incoming messages: parse, classify, and store the result.
        """
        message = self.parse_message(body)
        if not message:
            return
        # Perform classification
        prediction = self.classifier.predict(message)
        message['prediction'] = prediction
        classified_sightings.append(message)
        logger.info(f"Sighting ID {message.get('id')} classified as {prediction}")

    def start_consuming(self):
        """
        Start consuming messages from RabbitMQ. This call will block.
        """
        logger.info("Starting consumption of messages. Waiting for incoming sighting data...")
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self._on_message, auto_ack=True)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Stopping consumer and closing connection.")
            self.channel.stop_consuming()
            self.connection.close()
