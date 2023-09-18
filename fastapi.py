from fastapi import FastAPI, Query
from pymongo import MongoClient

app = FastAPI()

# MongoDB configuration - Replace with your MongoDB connection string
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["sensor_data"]  # Replace with your database name
collection = db["sensor_readings"]  # Replace with your collection name

@app.get("/sensor-readings/")
async def get_sensor_readings(
    start_date: str = Query(..., description="Start date in ISO8601 format"),
    end_date: str = Query(..., description="End date in ISO8601 format")
):
    try:
        # Query MongoDB for sensor readings within the specified range
        readings = list(collection.find({
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }))
        return {"sensor_readings": readings}
    except Exception as e:
        return {"error": str(e)}
