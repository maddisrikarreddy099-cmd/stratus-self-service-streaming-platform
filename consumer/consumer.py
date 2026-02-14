from confluent_kafka import Consumer
import json

BOOTSTRAP = "localhost:29092"
TOPIC = "stratus.events.raw"

conf = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": "stratus-consumer-group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

print("👂 Consumer started...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Consumer error:", msg.error())
            continue

        value = msg.value().decode("utf-8")
        event = json.loads(value)

        print("📩 Received Event:", event)

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
