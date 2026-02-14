import json
from kafka import KafkaProducer, KafkaConsumer

def load_config():
    with open("config/kafka_config.json") as f:
        return json.load(f)

def create_producer():
    config = load_config()
    return KafkaProducer(
        bootstrap_servers=config["bootstrap_servers"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def create_consumer():
    config = load_config()
    return KafkaConsumer(
        config["topic"],
        bootstrap_servers=config["bootstrap_servers"],
        group_id=config["consumer_group"],
        auto_offset_reset=config["auto_offset_reset"],
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
