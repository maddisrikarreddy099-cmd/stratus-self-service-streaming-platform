from confluent_kafka import Producer
import json
import time
import uuid
from faker import Faker

fake = Faker()

BOOTSTRAP = "localhost:29092"
TOPIC = "stratus.events.raw"

conf = {"bootstrap.servers": BOOTSTRAP}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"✅ Sent to {msg.topic()} [{msg.partition()}]")

print("🚀 Producer started...")

while True:
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "event_type": fake.random_element(elements=("click", "purchase", "login", "logout")),
        "timestamp": int(time.time() * 1000),
    }

    producer.produce(
        TOPIC,
        key=event["event_id"],
        value=json.dumps(event),
        callback=delivery_report
    )

    producer.poll(0)
    time.sleep(1)
