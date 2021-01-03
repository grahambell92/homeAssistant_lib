# Written by Graham Bell
# 17/04/2020

# This file is for a networked rpi zero to take photos.
import datetime
import sys
sys.path.append("../py_lib/")
from runWebcam_timelapse import webcam_timelapse
import os

webcam = webcam_timelapse(archiveBaseFolder='/home/graham/Downloads/',
                          cameraName='test',
                          cameraNumber='03')

motionComparionImg = webcam.archiveBaseFolder + 'motionPrev.jpg'

# ensure the archiveBaseFolder exists:
os.makedirs(webcam.archiveBaseFolder, exist_ok=True)

if True:
    webcam.motionSurveilance(
        timelapseInterval=30,
    )
