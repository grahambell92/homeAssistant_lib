# Written by Graham Bell
# 01/06/2019

# This file is for a networked rpi zero to take photos.
import sys
sys.path.append("../py_lib/")
from runWebcam_timelapse import webcam_timelapse
from rpiZeroParams import remoteCam0_settings as remoteCam_settings

import time

webcam = webcam_timelapse(archiveBaseFolder=remoteCam_settings['archiveBaseFolder'])

# Get largest img in archive folder

while True:
    # Get the list of most recent images.
    webcam.buildTimelapseGif(numImgs=remoteCam_settings['GifFrames'],
                             remoteCopyLocation=remoteCam_settings['haLiveGifPath'],
                             fps=remoteCam_settings['gifFPS'])
    print('Sleeping for', remoteCam_settings['buildGifEvery'], 'seconds')
    time.sleep(remoteCam_settings['buildGifEvery'])