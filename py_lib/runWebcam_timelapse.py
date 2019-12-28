# This file is for

import subprocess
import datetime
import itertools
import os
import shutil
import time
import imageio

class webcam_timelapse():
        def __init__(self, archiveBaseFolder='/home/pi/webcamImages/',):
                self.archiveBaseFolder = archiveBaseFolder
                currentDay = datetime.datetime.now().day
                daysCycle = itertools.cycle(range(3))
                imageCycler = itertools.count(250)
                dayCount = next(daysCycle)
                dayFolder = 'day{0}/'.format(dayCount)
                self.archiveFolder = self.archiveBaseFolder + dayFolder
                #print('hereere')

        def fireCamera(self, filePath):
            print('Firing camera...')
            # correct = subprocess.run(['fswebcam', '-r 640x480', '--quiet', filePath])
            correct = subprocess.run('fswebcam -r 640x480 --quiet --jpeg 50 {}'.format(filePath), shell=True)
            print('Done.')

        def scpImage(self):
                pass

        def copyToHAServer(self, currentImagePath, ):
                sshPass = 'sshpass -p "BlackWolf04"'
                # shouldn't need the pass because of ssh key installed.
                print('Trying to copy img to HA Server...')
                command = 'scp ~/webcamImages/currentImage.jpg homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/rpi_zero.jpg'
                correct = subprocess.run(command, shell=True)
                print('Done.')

        def copyTowwwFolder(self, currentImagePath):

                # Copy to the www folder for the HomeAssistant Server
                wwwFolder = '/home/homeassistant/.homeassistant/www/'
                os.makedirs(wwwFolder, exist_ok=True)
                shutil.copy(currentImagePath, wwwFolder)
                print('Copied to HA local folder:{}'.format(wwwFolder))


        def buildTimelapse(self, imgNum):
                # Make a gif of the most recent images

                lowImgNum = imgNum - 60
                if lowImgNum < 0:
                        lowImgNum = 0
                fileNames = [self.archiveFolder + 'image{0}.jpg'.format(i) for i in range(lowImgNum, imgNum)]


                currentGifPath = self.archiveFolder + 'currentSeq.gif'  # '/home/homeassistant/webcamImages/currentSeq$
                print(currentGifPath) 
                gifimages = []
                for fileName in fileNames:
                        try:
                                gifimages.append(imageio.imread(fileName))
                        except:
                                print('Unable to read:', fileName)
                imageio.mimsave(currentGifPath, gifimages)
                print('Saving current gif:', currentGifPath)
                exit(0)

        def rpiZero(self):
                currentDay = datetime.datetime.now().day
                self.daysCycle = itertools.cycle(range(3))
                self.imageCycler = itertools.count(250)
                dayCount = next(self.daysCycle)
                dayFolder = 'day{0}/'.format(dayCount)
                self.archiveFolder = self.archiveBaseFolder + dayFolder

                if os.path.exists(self.archiveFolder):
                        print('Existing archive directory, deleting.')
                        shutil.rmtree(self.archiveFolder)

                while True:
                        self.timelapse(sleepDuration=5, currentDay=currentDay, copyToHAServer=True)

        def timelapse(self, currentDay, sleepDuration=120, copyToHAServer=False):

                nowDay = datetime.datetime.now().day

                if nowDay != currentDay:
                        currentDay = nowDay
                        self.imageCycler = itertools.count()
                        dayCount = next(self.daysCycle)
                        if os.path.exists(archiveFolder):
                                print('Existing archive directory, deleting.')
                                shutil.rmtree(archiveFolder)

                # Take an image for the current image
                currentImagePath = self.archiveBaseFolder + 'currentImage.jpg'  # '~/webcamImages/currentImage$
                self.fireCamera(filePath=currentImagePath)

                # Move that current image to archive
                imgNum = next(self.imageCycler)

                archiveImage = 'image{0}.jpg'.format(imgNum)
                archivePath = self.archiveFolder + archiveImage
                # shutil.copy(currentImagePath, archiveFolder)
                # Create the directory if it doesnt exist
                os.makedirs(self.archiveFolder, exist_ok=True)
                shutil.copy(currentImagePath, archivePath)
                print('Archived image:{}'.format(archivePath))

                if copyToHAServer is True:
                        # self.copyToHAServer(currentImagePath=currentImagePath)
                        self.copyToHAServer(currentImagePath=currentImagePath)


                # Sleep delay for next image
                # sleepDuration = 120
                print('Sleeping for {} seconds.'.format(sleepDuration))
                time.sleep(sleepDuration)
                print('')

if __name__ == '__main__':
        webcam = webcam_timelapse()
        webcam.start()
        exit(0)


