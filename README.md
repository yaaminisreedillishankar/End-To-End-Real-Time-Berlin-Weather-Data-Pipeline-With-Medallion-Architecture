**🌦️ Real-Time Weather Analytics Pipeline (Berlin)**
An end-to-end Big Data solution utilizing a distributed Hadoop/Spark cluster to process and visualize Berlin's weather data through a Medallion Architecture. This project converts raw environmental telemetry into actionable business KPIs regarding energy costs and logistics risks.

**🏗️ Cluster Setup & Roles**
The pipeline runs on a distributed multi-node environment. Ensure all nodes are SSH-accessible.
Node,Role,Services
**Master:**"NameNode, ResourceManager","HDFS Master, YARN, Spark Master,
**Worker 1:**"DataNode, NodeManager","HDFS Storage, Spark Executor"
**Worker 2:**"DataNode, NodeManager","HDFS Storage, Spark Executor"

**Starting Services**
Execute these commands on the Master Node in order:

**Hadoop/HDFS:**
start-dfs.sh && start-yarn.sh

**Kafka (Zookeeper first):**
zookeeper-server-start.sh config/zookeeper.properties &
kafka-server-start.sh config/server.properties &

**InfluxDB:**
sudo systemctl start influxdb
systemctl is-active influxdb

**Grafana:**
# Reload systemd to recognize the new file
sudo systemctl daemon-reload

# Enable it to start on boot
sudo systemctl enable grafana

# Start the service
sudo systemctl start grafana

# Check the status again
sudo systemctl status grafana

🚀 How to Run the Pipeline
1. Initialize Kafka Topic
 kafka-topics.sh --create --topic weather_berlin --bootstrap-server localhost:9092 --partitions 3 --replication-factor 2

2. Start the Data Producer (Python)
Fetches data from Open-Meteo and pushes to Kafka.
python3 weather_producer.py

3. Submit the Spark Streaming Job
Processes data and writes to InfluxDB and HDFS.
spark-submit --master yarn \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,com.influxdb:influxdb-client-java:6.7.0 \
  spark_processor.py

Software,Version
Java,OpenJDK 11
Hadoop,3.3.x
Spark,3.3.x
Kafka,3.2.x
Python,"3.9+ (Libraries: kafka-python, requests)"
InfluxDB,2.x

📊 Monitoring & Visualization
Grafana Dashboard
Access: Navigate to http://<master-node-ip>:3000.

Data Source: Connect to InfluxDB using Flux (Port 8086).

Operational View: Live temperature, humidity, and wind trends for Berlin.

Business View: * Energy Surcharge ($): Hourly cost calculation for cooling.

Productivity Loss: Real-time man-hour risk audit.

System Health: Kafka consumer lag and Spark processing latency.

Resource Management
HDFS: http://localhost:8088/

InfluxDB: http://localhost:8086/

Grafana: http://localhost:3000/

📈 Business Logic (Gold Layer)
The pipeline doesn't just store data; it calculates:

Energy Loss: (Temp - 22°C) * $0.50 per hour.

Logistics Risk: High wind speeds (>50km/h) trigger "Critical" status in the Vulnerability Table.
