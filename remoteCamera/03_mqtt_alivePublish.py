import time
import paho.mqtt.client as paho
import datetime
from rpiZeroParams import remoteCam_settings



def on_message(client, userdata, message):
    time.sleep(1)
    print("Received message:", str(message.payload.decode("utf-8")))

brokerIP = remoteCam_settings['mqttBrokerIP'] # "192.168.0.55" #"10.0.0.19"
client = paho.Client(remoteCam_settings["mqttAliveClient"])

client.on_message = on_message
client.connect(brokerIP)
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

if False:
    # Hardware SPI configuration:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

if True:
    # Software SPI configuration.
    # Using GPIO pin numbers for spi connections.

    CLK = 2
    MISO = 3
    MOSI = 4
    CS = 17
    mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


while True:
    try:
        now = datetime.datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        msg = dt_string
        client.publish(remoteCam_settings["mqttAlivePublishTopic"], msg)
        time.sleep(120)

        if True:

            battRead = mcp.read_adc(0)
            #battVolt = 0.009821428 * battRead + 0.2558928 # for the outdoor camera battery
            # For the 12 v battery voltage divider with a 3.2 and a 9.9k ohm R2 and R1 combo.
            battVolt = 0.013052441*battRead + 0.004452565
            print('Battery voltage:', battVolt)
            if np.isfinite(battVolt):
                client.publish(remoteCam_settings["mqttBattVoltPublishTopic"], '{:.3f}'.format(battVolt))
            else:
                print('Bad battVolt:', battVolt)
    except:
        print('Failed to post MQTT message to', brokerIP)


client.disconnect() #disconnect
# client.loop_stop() #stop loop