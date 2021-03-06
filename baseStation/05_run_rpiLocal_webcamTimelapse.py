# This file is for 

import subprocess
import datetime
import itertools
import os
import shutil
import time
import imageio

def fireCamera(filePath):
    print('Firing camera...')
    # correct = subprocess.run(['fswebcam', '-r 640x480', '--quiet', filePath])
    correct = subprocess.run('fswebcam -r 640x480 --quiet --jpeg 50 {}'.format(filePath), shell=True)
    print('Done.')

currentDay = datetime.datetime.now().day
daysCycle = itertools.cycle(range(3))
imageCycler = itertools.count(250)

dayCount = next(daysCycle)
archiveFolder = '/home/homeassistant/webcamImages/day{0}/'.format(dayCount)

if os.path.exists(archiveFolder):
        print('Existing archive directory, deleting.')
        shutil.rmtree(archiveFolder)

while True:
        nowDay = datetime.datetime.now().day
        archiveFolder = '/home/homeassistant/webcamImages/day{0}/'.format(dayCount)
        
        if nowDay != currentDay:
                currentDay = nowDay
                imageCycler = itertools.count()
                dayCount = next(daysCycle)
                if os.path.exists(archiveFolder):
                        print('Existing archive directory, deleting.')
                        shutil.rmtree(archiveFolder)
        
        # Take an image for the current image
        currentImagePath = '/home/homeassistant/webcamImages/currentImage.jpg' # '~/webcamImages/currentImage$
        fireCamera(filePath=currentImagePath)
        
        # Move that current image to archive
        imgNum = next(imageCycler)

   	archiveImage = 'image{0}.jpg'.format(imgNum)
        archivePath = archiveFolder+archiveImage
        #shutil.copy(currentImagePath, archiveFolder)
        # Create the directory if it doesnt exist
        os.makedirs(archiveFolder, exist_ok=True)
        shutil.copy(currentImagePath, archivePath)
        print('Archived image:{}'.format(archivePath))


        # Make a gif of the most recent images
        if False:
                lowImgNum = imgNum -60
                if lowImgNum < 0:
                        lowImgNum = 0
                fileNames = [archiveFolder + 'image{0}.jpg'.format(i) for i in range(lowImgNum, imgNum)]

                currentGifPath = '/home/homeassistant/webcamImag	es/currentSeq.gif'
                currentGifPath = archiveFolder+'currentSeq.gif' #'/home/homeassistant/webcamImages/currentSeq$
        
                gifimages = []
                for fileName in fileNames:
                    gifimages.append(imageio.imread(fileName))
                imageio.mimsave(currentGifPath, gifimages)
                print('Saving current gif')
                exit(0)

        # Copy to the www folder for the HomeAssistant Server
        wwwFolder = '/home/homeassistant/.homeassistant/www/'
        os.makedirs(wwwFolder, exist_ok=True)
        shutil.copy(currentImagePath, wwwFolder)
        print('Copied to HA local folder:{}'.format(wwwFolder))

        # Sleep delay for next image
        sleepDuration = 120
        print('Sleeping for {} seconds.'.format(sleepDuration))
        time.sleep(sleepDuration)
        print('')
