# send_message.py

import pika
import json
import random
from datetime import datetime

def send_test_messages(n=10):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='ufo', exchange_type='fanout', durable=True)

    shapes = ['circle', 'triangle', 'square', 'oval']

    for i in range(n):
        message = {
            "id": f"sighting_{i}",
            "lat": random.uniform(-90, 90),
            "lon": random.uniform(-180, 180),
            "time": datetime.utcnow().isoformat(),
            "frequency": random.uniform(1.0, 100.0),
            "shape": random.choice(shapes),
            "msg": random.choice([
                "We have detected an alien communication signal",
                "Random noise from radar, nothing unusual",
                "Meteor spotted in the sky",
                "Signal repeats and shows intelligence"
            ])
        }
        body = json.dumps(message)
        channel.basic_publish(exchange='ufo', routing_key='', body=body)
        print(f"Sent: {message}")

    connection.close()

if __name__ == "__main__":
    send_test_messages(10)
