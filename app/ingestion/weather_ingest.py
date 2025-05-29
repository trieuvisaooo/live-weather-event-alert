import requests
import time
import json
from kafka import KafkaProducer
import os

API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
KAFKA_BROKER = os.environ.get("KAFKA_BROKER")
KAFKA_TOPIC = "weather_raw"

# Read cities and update interval from config/cities.json
with open("./config/cities.json", "r") as f:
    config = json.load(f)
    cities = config["cities"]
    update_interval = config.get("update_interval_seconds", 300)

print(f"Using Kafka broker: {KAFKA_BROKER}")
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode()
)

while True:
    for city in cities:
        city_name = city["name"]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
        print(f"Fetching weather for {city_name}...")
        res = requests.get(url).json()
        print(f"Sending weather data for {city_name} to Kafka topic '{KAFKA_TOPIC}'")
        producer.send(KAFKA_TOPIC, res)
    time.sleep(update_interval)  # every X seconds from config
