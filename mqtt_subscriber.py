import paho.mqtt.client as mqtt
import pymongo
import json

# MQTT broker configuration
mqtt_broker = "localhost"  # Replace with your MQTT broker's hostname or IP address
mqtt_port = 1883  # Default MQTT port
mqtt_topic_temperature = "sensors/temperature"
mqtt_topic_humidity = "sensors/humidity"

# MongoDB configuration - Update the connection string
try:
    print("works")	
    # Replace the connection string with your MongoDB Docker container's IP and port
    mongo_client = pymongo.MongoClient("mongodb://172.17.0.3:27017")
    print("works2")
    #db_names = mongo_client.list_database_names()
    #print("Connected to MongoDB. Available databases:", db_names)
    # Specify the database and collection you want to use
    mongo_db = mongo_client["sensor_readings"]
    mongo_collection = mongo_db["sensor_readings"]
except Exception as e:
    print("Error connecting to MongoDB:", str(e))

# Callback when a new MQTT message is received
def on_message(client, userdata, message):
    print("coming here")
    payload = message.payload.decode("utf-8")
    print("Received message on topic:", message.topic)
    print("Message payload:", payload)

    # Parse the JSON payload and store it in MongoDB
    try:
        print("works3")
        sensor_data = json.loads(payload)
        print("works3")
        mongo_collection.insert_one(sensor_data)
        print("Data stored in MongoDB")
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback function for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, keepalive=60, bind_address="")

# Subscribe to the MQTT topics
client.subscribe(mqtt_topic_temperature)
client.subscribe(mqtt_topic_humidity)

# Start the MQTT message loop
#client.loop_forever()
