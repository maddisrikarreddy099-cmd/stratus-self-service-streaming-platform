from common.kafka_client import create_consumer

consumer = create_consumer()

for message in consumer:
    print("Received:", message.value)
