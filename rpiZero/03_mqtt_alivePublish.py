import time
import paho.mqtt.client as paho
import datetime

def on_message(client, userdata, message):
    time.sleep(1)
    print("Received message:", str(message.payload.decode("utf-8")))

brokerIP = "10.0.0.19"
client = paho.Client("client-001")

client.on_message = on_message
client.connect(brokerIP)
print("publishing ")
while True:
    now = datetime.datetime.now()
    msg = 'Online as of: ' + str(now)
    client.publish("rpiSatTopic", msg)
    time.sleep(5)

client.disconnect() #disconnect
# client.loop_stop() #stop loop