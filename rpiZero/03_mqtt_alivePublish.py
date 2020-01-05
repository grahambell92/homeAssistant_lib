import time
import paho.mqtt.client as paho
import datetime

def on_message(client, userdata, message):
    time.sleep(1)
    print("Received message:", str(message.payload.decode("utf-8")))

brokerIP = "192.168.0.55" #"10.0.0.19"
client = paho.Client("client-001")

client.on_message = on_message
client.connect(brokerIP)
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))



while True:
    now = datetime.datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    msg = dt_string
    client.publish("rpiSatTopic", msg)
    time.sleep(30)

    if True:

        battRead = mcp.read_adc(0)
        battVolt = 0.009821428 * battRead + 0.2558928
        print('Battery voltage')
        client.publish("rpiZeroVoltageTopic", '{:.3f}'.format(battVolt))


client.disconnect() #disconnect
# client.loop_stop() #stop loop