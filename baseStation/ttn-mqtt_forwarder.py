
# fucking ttn doesn't maintain their docs. This is the mosquitto_sub info to grab my ttn application.
# mosquitto_sub -h thethings.meshed.com.au -u gbfarmdemo  -P 'ttn-account-v2.IIKE75n1Gc26zZVPmxD2172ZgDRAIiLQ9Eg0ZgEFvwI' -t '#'
# to just get one of the fields:
# mosquitto_sub -h thethings.meshed.com.au -u gbfarmdemo  -P 'ttn-account-v2.IIKE75n1Gc26zZVPmxD2172ZgDRAIiLQ9Eg0ZgEFvwI' -t '+/devices/+/up/digital_out_1'

# mqtt topic format to get an individual field
#my-app-id/devices/my-dev-id/up/water


# mosquitto_sub -h thethings.meshed.com.au -u gbfarmdemo  -P 'ttn-account-v2.IIKE75n1Gc26zZVPmxD2172ZgDRAIiLQ9Eg0ZgEFvwI' -t 'gbfarmdemo/devices/avenue_lasertripwire/up/digital_out_1'
# mosquitto_sub -h thethings.meshed.com.au -u gbfarmdemo  -P 'ttn-account-v2.IIKE75n1Gc26zZVPmxD2172ZgDRAIiLQ9Eg0ZgEFvwI' -t 'gbfarmdemo/devices/avenue_lasertripwire/up/presence_2'


# Taken from https://www.home-assistant.io/blog/2017/11/10/ttn-with-mqtt/

"""Relay MQTT messages from The Things Network to a local MQTT broker."""
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

DEVICE_NAME = 'avenue_lasertripwire'

TTN_BROKER = 'thethings.meshed.com.au'
TTN_USERNAME = 'gbfarmdemo'
TTN_PASSWORD = 'ttn-account-v2.IIKE75n1Gc26zZVPmxD2172ZgDRAIiLQ9Eg0ZgEFvwI'
# TTN_TOPIC = '+/devices/{}/up'.format(DEVICE_NAME)
TTN_TOPIC = 'gbfarmdemo/devices/avenue_lasertripwire/up/presence_2'
LOCAL_BROKER = '192.168.0.55'
LOCAL_TOPIC = 'gbfarmdemo/devices/avenue_lasertripwire/up/presence_2'


def on_connect(client, userdata, flags, rc):
    """Subscribe to topic after connection to broker is made."""
    print("Connected with result code", str(rc))
    client.subscribe(TTN_TOPIC)


def on_message(client, userdata, msg):
    """Relay message to a different broker."""
    # Convert from bytes object to literal string.
    # print(msg.payload.decode('UTF-8'))
    print('New message:', msg.payload.decode())
    publish.single(
        LOCAL_TOPIC, payload=msg.payload.decode(), qos=0, retain=False,
        hostname=LOCAL_BROKER, port=1883, client_id='ttn-local',
        keepalive=60, will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)


client = mqtt.Client()
client.username_pw_set(TTN_USERNAME, password=TTN_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.connect(TTN_BROKER, 1883, 60)

client.loop_forever()