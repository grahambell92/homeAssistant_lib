import time
import paho.mqtt.client as paho
import datetime

def on_message(client, userdata, message):
    time.sleep(1)
    print("Received message:", str(message.payload.decode("utf-8")))

brokerIP = "10.0.0.19"
client = paho.Client("client-001")

client.on_message = on_message

print("Connecting to broker:", brokerIP)
client.connect(brokerIP)

# client.loop_start() #start loop to process received messages

# print("subscribing ")
# client.subscribe("BrightnessTest")#subscribe

time.sleep(2)
print("publishing ")
while True:

    now = datetime.datetime.now()
    msg = 'Online as of: ' + str(now)
    client.publish("rpiSatTopic", msg)
    time.sleep(5)

client.disconnect() #disconnect
# client.loop_stop() #stop loop