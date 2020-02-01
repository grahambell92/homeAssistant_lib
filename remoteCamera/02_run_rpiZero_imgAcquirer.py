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
from rpiZeroParams import remoteCam0_settings as remoteCam_settings
import time

webcam = webcam_timelapse(archiveBaseFolder=remoteCam_settings['archiveBaseFolder'])
imageCountCycler = itertools.cycle(range(500))
motionComparionImg = webcam.archiveBaseFolder + 'motionPrev.jpg'

if os.path.exists(webcam.archiveFolder):
    print('Existing archive directory, deleting.')
    shutil.rmtree(webcam.archiveFolder)

while True:
    imgNum = next(imageCountCycler)
    webcam.takeAndArchive(imgArchiveNum=imgNum, sleepDuration=5, remoteCopyLocation=remoteCam_settings['haLiveImgPath'])
    for i in range(5):
        shutil.copy(webcam.currentImagePath, motionComparionImg)
        webcam.fireCamera(filePath=webcam.currentImagePath)
        webcam.motionCheck(currentImgPath=webcam.currentImagePath,
                           prevImgPath=motionComparionImg,
                           remoteCopyPath=remoteCam_settings['haLiveImgMotionPath'],
                           mqttBrokerIP=remoteCam_settings['haIP'],
                           motionThreshold=remoteCam_settings['motionThreshold'],
                           mqttMotionPublishTopic=remoteCam_settings['mqttMotionPublishTopic'],
                           mqttMotionClient=remoteCam_settings['mqttMotionClient'])
        time.sleep(5)
