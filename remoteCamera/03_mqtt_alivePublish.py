import time
import paho.mqtt.client as paho
import datetime
from rpiZeroParams import remoteCam_settings
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def on_message(client, userdata, message):
    time.sleep(1)
    print("Received message:", str(message.payload.decode("utf-8")))

def on_publish(client,userdata,result):             #create function for callback
    print("data published:", userdata)

brokerIP = remoteCam_settings['mqttBrokerIP'] # "192.168.0.55" #"10.0.0.19"
print('Setting up broker IP:', brokerIP)
client = paho.Client(remoteCam_settings["mqttClientName"])

client.on_message = on_message
client.connect(brokerIP)

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
    if False:
        try:
            now = datetime.datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            msg = dt_string
            print('Trying to publish...')
            print('Topic:', remoteCam_settings["mqttAlivePublishTopic"])
            print('Message:', msg)
            client.publish(remoteCam_settings["mqttAlivePublishTopic"], msg)
            print('Done.')
            print()

        except:
            print('Failed to post alive MQTT message to', brokerIP)

    if True:
        print('Reading adc for battery voltage...')
        battRead = mcp.read_adc(0)
        #battVolt = 0.009821428 * battRead + 0.2558928 # for the outdoor camera battery
        # For the 12 v battery voltage divider with a 3.2 and a 9.9k ohm R2 and R1 combo.
        battVolt = 0.013052441*battRead + 0.004452565
        print('Battery voltage:', battVolt)
        print('Done.')
        print(np.isfinite(battVolt))
        print()
        if np.isfinite(battVolt):
            print('Publishing battery voltage to:')
            print('Topic:', remoteCam_settings["mqttBattVoltPublishTopic"])
            msg = '{:.3f}'.format(battVolt)
            print('Msg:', msg)
            client.publish(remoteCam_settings["mqttBattVoltPublishTopic"], msg)
            print('Done')
        else:
            print('Bad battVolt:', battVolt)
        print()

        # except:
        #     print('Failed to post battery voltage MQTT message to', brokerIP)
    time.sleep(120)

client.disconnect() #disconnect
# client.loop_stop() #stop loop