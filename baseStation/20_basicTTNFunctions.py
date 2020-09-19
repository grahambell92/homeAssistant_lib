import time
import ttn

app_id = "whisperfarm-test"
access_key = "ttn-account-v2.17mYqE8Qa2T4eiuXnagd2mbxotOAmjDFcic_kA-Se9U"

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)

handler = ttn.HandlerClient(app_id, access_key)

# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()

payload = { "led_state": "on", "counter": 1 }
# oldPayload = base64.encodebytes(bytes("DATA YOU WANT TO SEND", 'utf-8')).decode()
mqtt_client.send("farmtest1", pay=payload, port=1, sched="replace")
# mqtt_client.send("device_id", )
# time.sleep(60)
mqtt_client.close()

if False:
  # using application manager client
  app_client = handler.application()
  my_app = app_client.get()
  print(my_app)
  my_devices = app_client.devices()
  print(my_devices)
