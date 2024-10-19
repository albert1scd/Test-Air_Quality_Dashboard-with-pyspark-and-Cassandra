from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg
from cassandra.cluster import Cluster
from cassandra.query import dict_factory
import json

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("AirQualityDashboard") \
    .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.0.0") \
    .config("spark.cassandra.connection.host", "localhost") \
    .getOrCreate()

# Initialize Cassandra connection
cluster = Cluster(['localhost'])
session = cluster.connect('air_quality')
session.row_factory = dict_factory

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Air Quality Dashboard API!"}

@app.get("/air-quality/{city}")
async def get_air_quality(city: str):
    try:
        # Read directly from Cassandra using Spark
        df = spark.read \
            .format("org.apache.spark.sql.cassandra") \
            .options(table="measurements", keyspace="air_quality") \
            .load()
        
        df = df.filter(col("city") == city)
        
        if df.count() == 0:
            raise HTTPException(status_code=404, detail=f"No data found for city: {city}")
        
        avg_aqi = df.agg(avg("aqi").alias("avg_aqi")).collect()[0]["avg_aqi"]
        max_aqi = df.agg({"aqi": "max"}).collect()[0]["max(aqi)"]
        
        latest_data = df.orderBy(col("timestamp").desc()).first()
        
        return {
            "city": city,
            "average_aqi": float(avg_aqi),
            "max_aqi": max_aqi,
            "latest_data": {
                "aqi": latest_data["aqi"],
                "pm25": latest_data["pm25"],
                "pm10": latest_data["pm10"],
                "no2": latest_data["no2"],
                "so2": latest_data["so2"],
                "co": latest_data["co"],
                "timestamp": str(latest_data["timestamp"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)