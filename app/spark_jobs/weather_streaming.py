from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col,  when
from pyspark.sql.types import StructType, StringType, FloatType, LongType, ArrayType, BooleanType
import os
import json

# db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
# engine = create_engine(db_url)

spark = SparkSession.builder.appName("WeatherAlertStream").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("name", StringType()) \
    .add("main", StructType() \
        .add("temp", FloatType()) \
        .add("humidity", FloatType())) \
    .add("wind", StructType() \
        .add("speed", FloatType())) \
    .add("weather", ArrayType(StructType() \
        .add("description", StringType()))) \
    .add("dt", LongType()) \
    .add("is_alert", BooleanType(), nullable=True)

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", os.getenv("KAFKA_BROKER", "kafka:29092")) \
    .option("subscribe", "weather_raw") \
    .option("startingOffsets", "earliest") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select(
        col("data.name").alias("city"),
        col("data.dt").alias("timestamp"),
        col("data.main.temp").alias("temperature"),
        col("data.weather")[0]["description"].alias("weather"),
        col("data.main.humidity").alias("humidity"),
        col("data.wind.speed").alias("wind_speed"),
        col("data.is_alert").alias("is_alert") 
    )

# Example condition: heat alert
with open("./config/alert_thresholds.json", "r") as f:
    config = json.load(f)
    alert_thresholds = config["alert_thresholds"]
    temperature_threshold = alert_thresholds["temperature"]
    wind_speed_threshold = alert_thresholds["wind_speed"]

json_df = json_df.withColumn(
    "is_alert", when(
        (col("temperature") < temperature_threshold["low"]) |
        (col("temperature") > temperature_threshold["high"]) |
        (col("wind_speed") > wind_speed_threshold["high"]),
        True  
    ).otherwise(False)  
)

json_df = json_df.withColumn("temperature", (col("temperature") - 273.15))


# json_df.writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .start() \
#     .awaitTermination()
    
jdbc_url = f"jdbc:postgresql://db:5432/{os.getenv('POSTGRES_DB')}"
jdbc_properties = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "driver": "org.postgresql.Driver"
}

# Write to PostgreSQL using foreachBatch
def write_to_postgres(batch_df, batch_id):
    batch_df.write.jdbc(
        url=jdbc_url,
        table="weather_alerts",  
        mode="append",
        properties=jdbc_properties
    )
    print(f"[BATCH {batch_id}] Wrote {batch_df.count()} records to PostgreSQL successfully.")

# Streaming write
json_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/spark_weather_alerts_checkpoint") \
    .start() \
    .awaitTermination()
