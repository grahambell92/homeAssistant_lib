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
from rpiZeroParams import remoteCam_settings
import time

for key,value in remoteCam_settings.items():
    print(key, value)

webcam = webcam_timelapse(archiveBaseFolder=remoteCam_settings['archiveBaseFolder'],
                          cameraName=remoteCam_settings['cameraName'],
                          cameraNumber=remoteCam_settings['cameraNumber'])

imageCountCycler = itertools.cycle(range(500))
motionComparionImg = webcam.archiveBaseFolder + 'motionPrev.jpg'

if os.path.exists(webcam.archiveFolder):
    print('Existing archive directory, deleting.')
    shutil.rmtree(webcam.archiveFolder)

while True:
    imgNum = next(imageCountCycler)
    webcam.removeOldDayOfYearFolders()
    webcam.takeAndArchive(imgArchiveNum=imgNum, sleepDuration=5, remoteCopyLocation=remoteCam_settings['haLiveImgPath'],
                          quality=remoteCam_settings['imgQuality'],
                          flipVert=remoteCam_settings['flipVert'],
                          flipHorz=remoteCam_settings['flipHori']
                          )
    for i in range(5):
        shutil.copy(webcam.currentImagePath, motionComparionImg)
        webcam.fireCamera(filePath=webcam.currentImagePath,
                          quality=remoteCam_settings['imgQuality'],
                          flipVert=remoteCam_settings['flipVert'],
                          flipHorz=remoteCam_settings['flipHori'])
        if True:
            webcam.motionCheck(currentImgPath=webcam.currentImagePath,
                               prevImgPath=motionComparionImg,
                               remoteCopyPath=remoteCam_settings['haLiveImgMotionPath'],
                               mqttBrokerIP=remoteCam_settings['mqttBrokerIP'],
                               motionThreshold=remoteCam_settings['motionThreshold'],
                               mqttMotionPublishTopic=remoteCam_settings['mqttMotionPublishTopic'],
                               mqttMotionClient=remoteCam_settings['mqttMotionClient'])
        time.sleep(5)
