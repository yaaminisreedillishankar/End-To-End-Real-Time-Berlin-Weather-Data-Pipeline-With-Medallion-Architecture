from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from datetime import datetime

# 1. Configuration
TOKEN = "zYAd-bo9VOVh2NJ_YswyJ0nMWgU07WKu1is1uhAapnaZcwXqcPQD8kmBxeCgvEFhWa8C5eR6wg7RqVrJvzsq0Q=="
ORG = "M2_CSDS"
BUCKET = "weather_analytics"
URL = "http://10.0.0.63:8086"

# 2. Initialize Spark
spark = SparkSession.builder \
    .appName("SilverToInflux_Final_Fix") \
    .getOrCreate()

# 3. Read from the Silver path (which we confirmed exists)
silver_path = "/silver/weather"
silver_df = spark.read.parquet(silver_path)

# 4. Select the columns that actually exist in your Silver schema
# Based on your previous error, these are: city, temperature_2m, wind_speed_10m, event_time
df_to_push = silver_df.select(
    "city",
    col("temperature_2m").alias("temp"),
    col("wind_speed_10m").alias("wind"),
    col("event_time").alias("timestamp")
)

# 5. Convert to Pandas for iteration
data_rows = df_to_push.toPandas()

# 6. Connect and Write to InfluxDB
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

print(f"🚀 Found {len(data_rows)} rows. Pushing to InfluxDB...")

for _, row in data_rows.iterrows():
    # Convert string timestamp to datetime object
    try:
        # Handles ISO format like 2026-01-15T14:00:00
        dt = datetime.fromisoformat(str(row['timestamp']).replace('Z', '+00:00'))
    except ValueError:
        # Fallback for other formats
        dt = datetime.strptime(str(row['timestamp']), '%Y-%m-%d %H:%M:%S')

    point = Point("weather_metrics") \
        .tag("city", row['city']) \
        .field("temp", float(row['temp'])) \
        .field("wind", float(row['wind'])) \
        .time(dt)

    write_api.write(bucket=BUCKET, org=ORG, record=point)

client.close()
spark.stop()
print("✅ Dashboard Sync Complete!")
