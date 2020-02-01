import time, string
import serial
import paho.mqtt.client as paho
from readSerial2 import decode_float

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

time.sleep(1)
ser.flushInput();  # clean input buffer

brokerIP = "192.168.0.55" #"10.0.0.19"
client = paho.Client("client-002")
client.connect(brokerIP)

while True:
    print('waiting...')
    value = ser.readline()
    num = decode_float(value[2:10])
    print(num)
    if type(num) == float:
        client.publish("brightnessTopic3", num)
        print('Mqtt Published ok.')

client.disconnect() #disconnect