# Dictates the parameters for this camera system

rpiSettings = {
    'archiveBaseFolder': '/home/pi/webcamImages/',

    'haLiveImgPath': 'homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/rpi_zero.jpg',
    'haLiveImgMotionPath': 'homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/rpi_zero_motion.jpg',
    'haLiveGifPath': 'homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/rpi_timelapse.gif',

    # Gif timelapse building properties.
    'buildGifEvery': 120, # Seconds
    'GifFrames': 15,
    'gifFPS': 3, # Frames per second.

}

