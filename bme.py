

import time
import board
import adafruit_bme280
import ssl
import paho.mqtt.client as mqtt

# Set up BME280 sensor object
i2c = board.I2C()
bme280 = Adafruit_BME280_I2C(i2c=i2c)
# Define AWS IoT endpoint, port, and topic
endpoint = "a2xq8cwzxe9fd1-ats.iot.ap-northeast-1.amazonaws.com"
port = 8883
topic = "YOUR_TOPIC"

# Set up MQTT client and connect to AWS IoT endpoint using SSL/TLS encryption
client = mqtt.Client()
client.tls_set(
    ca_certs="root-CA.crt",
    certfile="Coco.cert.pem",
    keyfile="Coco.private.key",
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2,
    ciphers=None
)
client.connect(endpoint, port=port)

# In a loop, read sensor data and publish it to AWS IoT topic using MQTT
while True:
    temperature = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure
    payload = '{{"temperature": {:.2f}, "humidity": {:.2f}, "pressure": {:.2f}}}'.format(
        temperature, humidity, pressure)
    client.publish(topic, payload)
    print("Published:", payload)
    time.sleep(5)

