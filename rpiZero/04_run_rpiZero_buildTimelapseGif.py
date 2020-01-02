# Written by Graham Bell
# 01/06/2019

# This file is for a networked rpi zero to take photos.
import sys
sys.path.append("../py_lib/")
from runWebcam_timelapse import webcam_timelapse
from 00_rpiZeroParams import rpiSettings
import time
from glob import glob

webcam = webcam_timelapse(archiveBaseFolder=rpiSettings['archiveBaseFolder'])

# Get largest img in archive folder

while True:
    # Get the list of most recent images.
    webcam.buildTimelapseGif(numImgs=rpiSettings['GifFrames'], remoteCopyLocation=rpiSettings['haLiveGifPath'], fps=rpiSettings['gifFPS'])

    time.sleep(rpiSettings['buildGifEvery'])