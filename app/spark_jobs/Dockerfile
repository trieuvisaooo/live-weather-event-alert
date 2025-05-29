FROM bitnami/spark:latest

USER root
WORKDIR /app

COPY . .

USER 1001

# If you have Python dependencies for Spark jobs:
RUN pip install --no-cache-dir -r requirements.txt

CMD ["spark-submit", "--master", "local[*]", "/app/weather_streaming.py"]