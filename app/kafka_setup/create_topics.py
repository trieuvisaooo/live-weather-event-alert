import time
from kafka.admin import KafkaAdminClient, NewTopic
import os

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:29092")

topics = [
    NewTopic(name="weather_raw", num_partitions=1, replication_factor=1),
    NewTopic(name="weather_alerts", num_partitions=1, replication_factor=1),
]

# Wait for Kafka to be fully ready
time.sleep(10)

try:
    print(f"Creating topics on {KAFKA_BROKER}")
    admin = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER,
        client_id='topic-creator'
    )
    existing = admin.list_topics()

    for topic in topics:
        if topic.name not in existing:
            print(f"Creating topic: {topic.name}")
            admin.create_topics([topic])
        else:
            print(f"Topic already exists: {topic.name}")

except Exception as e:
    print("Failed to create topics:", e)
