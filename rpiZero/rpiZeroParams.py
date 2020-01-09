# Dictates the parameters for this camera system

haIP = "192.168.0.55" # "10.0.0.19"
rpiSettings = {
    'archiveBaseFolder': '/home/pi/webcamImages/',

    'haLiveImgPath': 'homeassistant@' + haIP + ':/home/homeassistant/.homeassistant/www/rpi_zero.jpg',
    'haLiveImgMotionPath': 'homeassistant@' + haIP + ':/home/homeassistant/.homeassistant/www/rpi_zero_motion.jpg',
    'haLiveGifPath': 'homeassistant@' + haIP + ':/home/homeassistant/.homeassistant/www/rpi_timelapse.gif',

    # Gif timelapse building properties.
    'buildGifEvery': 180, # Seconds
    'GifFrames': 8,
    'gifFPS': 2, # Frames per second.

}

