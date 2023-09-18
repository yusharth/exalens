import paho.mqtt.client as mqtt
import json
import random
import time
from datetime import datetime

# MQTT broker configuration
mqtt_broker = "localhost"  # Replace with your MQTT broker's address
mqtt_port = 1883  # Default MQTT port
mqtt_topic_temperature = "sensors/temperature"
mqtt_topic_humidity = "sensors/humidity"

# Function to generate a random sensor reading
def generate_sensor_reading():
    sensor_id = "unique_sensor_id"
    value = random.uniform(0, 100)  # Random value between 0 and 100
    timestamp = datetime.utcnow().isoformat()
    payload = {
        "sensor_id": sensor_id,
        "value": value,
        "timestamp": timestamp
    }
    return json.dumps(payload)

# Callback when the MQTT client connects
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed with code", rc)

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, keepalive=60)

# Main loop to publish sensor readings
try:
    while True:
        temperature_reading = generate_sensor_reading()
        humidity_reading = generate_sensor_reading()

        # Publish readings to MQTT topics
        client.publish(mqtt_topic_temperature, temperature_reading)
        client.publish(mqtt_topic_humidity, humidity_reading)

        print("Published temperature:", temperature_reading)
        print("Published humidity:", humidity_reading)

        time.sleep(5)  # Publish readings every 5 seconds

except KeyboardInterrupt:
    print("MQTT publisher terminated by user")

# Disconnect from the MQTT broker
client.disconnect()
