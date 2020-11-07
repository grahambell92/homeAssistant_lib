# Written by Graham Bell
# 17/04/2020

# This file is for a networked rpi zero to take photos.
import datetime
import sys
sys.path.append("../py_lib/")
from runWebcam_timelapse import webcam_timelapse
import os
import shutil
from rpiZeroParams import remoteCam_settings
import time

webcam = webcam_timelapse(archiveBaseFolder=remoteCam_settings['archiveBaseFolder'],
                          cameraName=remoteCam_settings['cameraName'],
                          cameraNumber=remoteCam_settings['cameraNumber'])

motionComparionImg = webcam.archiveBaseFolder + 'motionPrev.jpg'

# ensure the archiveBaseFolder exists:
os.makedirs(webcam.archiveBaseFolder, exist_ok=True)


if True:
    while True:
        webcam.takeAndArchive(
            remoteCopyLocation_LQ=remoteCam_settings['haLiveImgPath_LQ'],
            remoteCopyLocation_HQ=remoteCam_settings['haLiveImgPath_HQ'],
            remoteArchiveFolder=remoteCam_settings['haArchiveSCPFolderPath'],
            quality=remoteCam_settings['imgQuality'],
            cameraResolution=(3280, 2464),
            flipVert=remoteCam_settings['flipVert'],
            flipHorz=remoteCam_settings['flipHori'],
        )
        time.sleep(30)

if False:
    webcam.motionSurveilance(
        remoteCopyLocation_LQ=remoteCam_settings['haLiveImgPath_LQ'],
        remoteCopyLocation_HQ=remoteCam_settings['haLiveImgPath_HQ'],
        remoteArchiveFolder=remoteCam_settings['haArchiveSCPFolderPath'],
        quality=remoteCam_settings['imgQuality'],
        flipVert=remoteCam_settings['flipVert'],
        flipHorz=remoteCam_settings['flipHori'],
        timelapseInterval=180,
    )
