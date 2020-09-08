import time
import paho.mqtt.client as paho
import datetime
from rpiZeroParams import remoteCam_settings
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import numpy as np

def on_message(client, userdata, message):
    time.sleep(1)
    print("Received message:", str(message.payload.decode("utf-8")))

def on_publish(client,userdata,result):             #create function for callback
    print("data published:", userdata)



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

battVolts = []
battVolt_median = np.nan

timeBetweenAlivePosts = 30.0
timeBetweenBattVoltPosts = 60.0
timeBetweenBattReads = 3.0

timeOfLastBattPost = time.time() - 100.0
timeOfLastBattRead = time.time() - 100.0
timeOfLastAlivePost = time.time() - 100.0

def connectToBroker():
    try:
        # Reconnect to the broker each time prevents the HA server from being unable to find new events.
        # The broker reaches out and connects with the mosquitto server each time.

        brokerIP = remoteCam_settings['mqttBrokerIP']  # "192.168.0.55" #"10.0.0.19"
        print('Setting up broker IP:', brokerIP)
        client = paho.Client(remoteCam_settings["mqttClientName"])

        client.on_message = on_message
        client.connect(brokerIP)
        return client

    except:
        print('Failed to connect to broker IP.')

while True:
    timeSinceLastBattPost = time.time() - timeOfLastBattPost
    timeSinceLastBattRead = time.time() - timeOfLastBattRead
    timeSinceLastAlivePost = time.time() - timeOfLastAlivePost

    if False:
        print('Time since last batt post', timeSinceLastBattPost)
        print('Time since last alive post', timeSinceLastAlivePost)
        print('Time since last batt read', timeSinceLastBattRead)

    if np.isnan(battVolt_median):
        timeOfLastBattPost = time.time()


    if timeSinceLastBattPost > timeBetweenBattVoltPosts:
        client = connectToBroker()

        try:
            if np.isfinite(battVolt_median):
                print('Publishing battery voltage to:')
                print('Topic:', remoteCam_settings["mqttBattVoltPublishTopic"])
                msg = '{:.3f}'.format(battVolt_median)
                print('Msg:', msg)
                client.publish(remoteCam_settings["mqttBattVoltPublishTopic"], msg)
                print('Done')
            else:
                print('Bad battVolt:', battVolt_median)
            print()

        except:
            brokerIP = remoteCam_settings['mqttBrokerIP']  # "192.168.0.55" #"10.0.0.19"
            print('Failed to post median battery voltage MQTT message to', brokerIP)

        timeOfLastBattPost = time.time()

    if timeSinceLastAlivePost > timeBetweenAlivePosts:
        client = connectToBroker()

        try:
            msg = 'online'
            print('Trying to publish...')
            print('Topic:', remoteCam_settings["mqttAlivePublishTopic"])
            print('Message:', msg)
            client.publish(remoteCam_settings["mqttAlivePublishTopic"], msg)
            print('Done.')
            print()

        except:
            brokerIP = remoteCam_settings['mqttBrokerIP']  # "192.168.0.55" #"10.0.0.19"
            print('Failed to post alive MQTT message to', brokerIP)

        timeOfLastAlivePost = time.time()

    if timeSinceLastBattRead > timeBetweenBattReads:
        # Read the battery voltage and do a rolling median on the value
        print('Reading adc for battery voltage...')
        battRead = mcp.read_adc(0)
        # battVolt = 0.009821428 * battRead + 0.2558928 # for the outdoor camera battery
        # For the 12 v battery voltage divider with a 3.2 and a 9.9k ohm R2 and R1 combo.
        battVolt = 0.013052441 * battRead + 0.004452565
        print('Battery voltage:', battVolt)

        if np.isfinite(battVolt):
            battVolts.append(battVolt)


        if len(battVolts) > 20:
            # remove the first value from the list
            battVolts.pop(0)

        median = np.median(battVolts)
        if np.isfinite(median):
            battVolt_median = median

        else:
            print('Batt volt error: Median calculation contains bad value.')
            battVolt_median = np.nan

        # print('Batt volt median', battVolt_median)
        # print('Battvolts:', battVolts)

        timeOfLastBattRead = time.time()

    print('')
    time.sleep(1.0) # Just slow the code down here so it isn't constantly checking the time.



client.disconnect() #disconnect
# client.loop_stop() #stop loop