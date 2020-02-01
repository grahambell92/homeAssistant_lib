# Dictates the parameters for this camera system

haIP = "192.168.0.55" # "10.0.0.19"
haFolder = '/home/pi/homeassistant/'
haUser = 'pi'

remoteCam0_settings = {
    'archiveBaseFolder': '/home/pi/webcamImages/',
    'haLiveImgPath': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam0_currentImage.jpg',
    'haLiveImgMotionPath': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam0_lastMotion.jpg',
    'haLiveGifPath': haUser + '@' + haIP + ':' + haFolder + 'www/remoteCam0_timelapse.gif',

    # Gif timelapse building properties.
    'buildGifEvery': 180, # Seconds
    'GifFrames': 8,
    'gifFPS': 2, # Frames per second.

}

