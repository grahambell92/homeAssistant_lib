# Written by Graham Bell
# 01/06/2019

# This file is for a networked rpi zero to take photos.
import datetime
import itertools
import sys
sys.path.append("../py_lib/")
from runWebcam_timelapse import webcam_timelapse
import os
import shutil
from rpiZeroParams import rpiSettings
import time

webcam = webcam_timelapse(archiveBaseFolder=rpiSettings['archiveBaseFolder'])
imageCountCycler = itertools.cycle(range(500))

if os.path.exists(webcam.archiveFolder):
    print('Existing archive directory, deleting.')
    shutil.rmtree(webcam.archiveFolder)

while True:
    imgNum = next(imageCountCycler)
    webcam.takeAndArchive(imgArchiveNum=imgNum, sleepDuration=5, remoteCopyLocation=rpiSettings['haLiveImgPath'])
    for i in range(5):
        webcam.fireCamera(filePath=webcam.currentImagePath)
        webcam.motionCheck(currentImgPath=webcam.currentImagePath, prevImgPath=webcam.currentArchivePath)
        time.sleep(5)
