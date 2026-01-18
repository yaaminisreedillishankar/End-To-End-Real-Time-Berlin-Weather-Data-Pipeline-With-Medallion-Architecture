from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, min, max, count, round

spark = SparkSession.builder \
    .appName("Weather-Silver-To-Gold") \
    .getOrCreate()

# 1. Read the Clean Silver data
silver_path = "/silver/weather"
df_silver = spark.read.parquet(silver_path)

# 2. Aggregate data (Daily Summary)
df_gold = df_silver.groupBy("city", "date").agg(
    round(avg("temperature_2m"), 2).alias("avg_temp"),
    min("temperature_2m").alias("min_temp"),
    max("temperature_2m").alias("max_temp"),
    count("event_ts").alias("total_readings")
)

# 3. Write to the Gold layer
# Note: Gold data is usually small, so we don't always need complex partitioning
gold_path = "/gold/weather_daily_summary"

df_gold.write \
    .mode("overwrite") \
    .parquet(gold_path)

print("Gold layer updated successfully.")
df_gold.show()

spark.stop()
