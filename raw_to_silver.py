from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Weather-Raw-To-Silver") \
    .getOrCreate()

# 1. Read the Raw data we just generated
raw_path = "/raw/weather"
df_raw = spark.read.parquet(raw_path)

# 2. Remove duplicates
# We define uniqueness by the combination of city and the timestamp
df_silver = df_raw.dropDuplicates(["city", "event_ts"])

# 3. Write to the Silver layer
# We still partition by date/hour for fast queries later
silver_path = "/silver/weather"

df_silver.write \
    .mode("overwrite") \
    .partitionBy("date", "hour") \
    .parquet(silver_path)

print(f"Silver layer updated. Rows before: {df_raw.count()} | Rows after: {df_silver.count()}")

spark.stop()
