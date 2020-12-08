

import sys
sys.path.append("../py_lib/")
from runWebcam_timelapse import webcam_timelapse
print('Removing old webcam image folders....')

baseStationImgArchiveFolder = '/home/pi/basestationData/cameraImageArchive/'
webcam = webcam_timelapse(archiveBaseFolder=baseStationImgArchiveFolder)
webcam.daysToKeep = 20

webcam.removeOldDayOfYearFolders()

print('Done. Exiting.')