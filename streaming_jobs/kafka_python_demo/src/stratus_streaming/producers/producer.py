import time
from common.kafka_client import create_producer

producer = create_producer()

while True:
    message = {
        "message": "Hello Stratus",
        "timestamp": time.time()
    }

    producer.send("test-topic", message)
    print("Sent:", message)

    time.sleep(2)
