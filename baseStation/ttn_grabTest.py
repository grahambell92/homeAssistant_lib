import time
import ttn

app_id = "gbfarmdemo"
access_key = "ttn-account-v2.IIKE75n1Gc26zZVPmxD2172ZgDRAIiLQ9Eg0ZgEFvwI"

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg['payload'])

handler = ttn.HandlerClient(app_id, access_key)

while True:
    # using mqtt client
    mqtt_client = handler.data()
    mqtt_client.set_uplink_callback(uplink_callback)

    mqtt_client.connect()

    # print('Connecting...')
    # time.sleep(1)
    # mqtt_client.close()

if False:
    # using application manager client
    app_client =  handler.application()
    my_app = app_client.get()
    print(my_app)
    my_devices = app_client.devices()
    print(my_devices)
