# Dictates the parameters for this camera system

haIP = "192.168.0.55" # "10.0.0.19"
haFolder = '/home/pi/homeassistant/'
baseStationImgArchiveFolder = '/home/pi/basestationData/cameraImageArchive/'

haUser = 'pi'

cameraNames = {
    'avenue': 0,
    'yard'  : 1,
    'windmill': 2,
    'mintos': 3,
}

remoteCam0_Settings = {

    'macAddress': '',

    'cameraName': 'avenue',
    'archiveBaseFolder': '/home/pi/webcamImages/',

    'haLiveImgPath_LQ': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam0_currentImage_LQ.jpg',
    'haLiveImgPath_HQ': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam0_currentImage_HQ.jpg',

    'haLiveImgMotionPath': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam0_lastMotion.jpg',
    'haLiveGifPath': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam0_timelapse.gif',

    'haArchiveSCPFolderPath': haUser + '@' + haIP + ':' + baseStationImgArchiveFolder,

    # Rpi camera settings
    'imgQuality': 10,
    'flipVert': True,
    'flipHori': True,

    # Gif timelapse building properties.
    'buildGifEvery': 60, # Seconds
    'GifFrames': 8,
    'gifFPS': 2, # Frames per second.

    # Motion MQTT reporting properties.
    'mqttBrokerIP': haIP,
    'motionThreshold': 6.0, # Just a threshold.
    'mqttMotionClient': "remoteCamera0_motion",
    'mqttMotionPublishTopic': "remoteCamera0/motionValue",

    # MQTT Alive reporting properties.
    'mqttAliveClient': "remoteCamera0_lastPing",
    'mqttAlivePublishTopic': "remoteCamera0/lastPing",
    'mqttBattVoltPublishTopic': "remoteCamera0/battVoltage",

}


remoteCam1_settings = {

    'cameraName': 'yard',

    'archiveBaseFolder': '/home/pi/webcamImages/',

    'haLiveImgPath_LQ': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam1_currentImage_LQ.jpg',
    'haLiveImgPath_HQ': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam1_currentImage_HQ.jpg',

    'haLiveImgMotionPath': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam1_lastMotion.jpg',
    'haLiveGifPath': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam1_timelapse.gif',

    'haArchiveSCPFolderPath': haUser + '@' + haIP + ':' + baseStationImgArchiveFolder,

    # Rpi camera settings
    'imgQuality': 10,
    'flipVert': True,
    'flipHori': True,

    # Gif timelapse building properties.
    'buildGifEvery': 60, # Seconds
    'GifFrames': 8,
    'gifFPS': 2, # Frames per second.

    # Motion MQTT reporting properties.
    'mqttBrokerIP': haIP,
    'motionThreshold': 6.0, # Just a threshold.
    'mqttMotionClient': "remoteCamera1_motion",
    'mqttMotionPublishTopic': "remoteCamera1/motionValue",

    # MQTT Alive reporting properties.
    'mqttAliveClient': "remoteCamera1_lastPing",
    'mqttAlivePublishTopic': "remoteCamera1/lastPing",
    'mqttBattVoltPublishTopic': "remoteCamera1/battVoltage",

}

macAddressDict = {
    202481595754817: remoteCam0_Settings,
    64425562547: remoteCam1_settings
}

from uuid import getnode as get_mac
macAddress = get_mac()
remoteCam_settings = macAddressDict[macAddress]

dicts = [remoteCam0_Settings, remoteCam1_settings]
for dict in dicts:
    dict['cameraNumber'] = cameraNames[dict['cameraName']]

