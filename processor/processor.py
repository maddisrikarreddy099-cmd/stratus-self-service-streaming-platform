from confluent_kafka import Consumer, Producer
import json
import time
from prometheus_client import Counter, start_http_server

BOOTSTRAP = "localhost:29092"

RAW_TOPIC = "stratus.events.raw"
ENRICHED_TOPIC = "stratus.events.enriched"
DLQ_TOPIC = "stratus.events.dlq"

# ✅ Prometheus Metrics
events_processed_total = Counter(
    "events_processed_total",
    "Total successfully processed events"
)

events_failed_total = Counter(
    "events_failed_total",
    "Total failed events sent to DLQ"
)

required_fields = ["event_id", "user_id", "event_type", "timestamp"]

def validate_event(event: dict):
    # Example: force failures for testing DLQ
    if event.get("event_type") == "logout":
        raise ValueError("Forced failure for DLQ testing")

    for field in required_fields:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")

    if event["event_type"] not in ["click", "purchase", "login", "logout"]:
        raise ValueError("Invalid event_type")


def enrich_event(event: dict):
    event["processed_ts"] = int(time.time() * 1000)
    event["pipeline"] = "stratus-core"
    return event


consumer_conf = {
    "bootstrap.servers": BOOTSTRAP,
    "group.id": "stratus-processor-group",
    "auto.offset.reset": "earliest",
}

producer_conf = {"bootstrap.servers": BOOTSTRAP}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe([RAW_TOPIC])

# ✅ Start Prometheus HTTP endpoint
start_http_server(8001)
print("📊 Metrics running at http://localhost:8001")
print("⚙️ Processor started...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print("Consumer error:", msg.error())
            continue

        raw_value = msg.value().decode("utf-8")

        try:
            event = json.loads(raw_value)

            validate_event(event)
            enriched = enrich_event(event)

            producer.produce(
                ENRICHED_TOPIC,
                key=msg.key(),
                value=json.dumps(enriched)
            )
            producer.poll(0)

            events_processed_total.inc()
            print(f"✅ Processed event {event['event_id']}")

        except Exception as e:
            print(f"❌ Processing failed: {e}")

            # Send original raw payload to DLQ
            producer.produce(
                DLQ_TOPIC,
                key=msg.key(),
                value=raw_value
            )
            producer.poll(0)

            events_failed_total.inc()
            print("⚠️ Sent event to DLQ")

except KeyboardInterrupt:
    print("Shutting down processor...")

finally:
    consumer.close()
    producer.flush()
