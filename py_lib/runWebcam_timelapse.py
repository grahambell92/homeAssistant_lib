# This file is for

import subprocess
import datetime
import itertools
import os
import shutil
import time
import imageio
from PIL import Image, ImageFilter
import numpy as np
import paho.mqtt.client as paho

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

        def copyToHAServer(self, inputFilePath, outputFilePath='rpi_zero.jpg'):
                sshPass = 'sshpass -p "BlackWolf04"'
                # shouldn't need the passwd because of ssh key installed.
                print('Trying to copy img to HA Server...')
                # inputFilePath = '~/webcamImages/currentImage.jpg'
                # outputFilePath = 'homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/'
                # command = 'scp ~/webcamImages/currentImage.jpg homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/'
                command = ' '.join(['scp', inputFilePath, outputFilePath]) #scp' + inputFilePath + outputFilePath
                correct = subprocess.run(command, shell=True)
                print('Done.')

        def copyTowwwFolder(self, currentImagePath):

                # Copy to the www folder for the HomeAssistant Server
                wwwFolder = '/home/homeassistant/.homeassistant/www/'
                os.makedirs(wwwFolder, exist_ok=True)
                shutil.copy(currentImagePath, wwwFolder)
                print('Copied to HA local folder:{}'.format(wwwFolder))


        def buildTimelapse(self, imgNum, numImgs=10):
                # Make a gif of the most recent images

                lowImgNum = imgNum - 10
                if lowImgNum < 0:
                        lowImgNum = 0
                fileNames = [self.archiveFolder + 'image{0}.jpg'.format(i) for i in range(lowImgNum, imgNum+1)]


                currentGifPath = self.archiveFolder + 'currentSeq.gif'  # '/home/homeassistant/webcamImages/currentSeq$
                print(currentGifPath) 
                gifimages = []
                for fileName in fileNames:
                        try:
                                gifimages.append(imageio.imread(fileName))
                                print('Appended:', fileName)
                        except:
                                print('Unable to read:', fileName)
                if len(gifimages) > 0:

                        imageio.mimsave(currentGifPath, gifimages)
                        print('Saving current gif:', currentGifPath)
                        outputFilePath = 'homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/rpi_timelapse.gif'
                        self.copyToHAServer(inputFilePath=currentGifPath, outputFilePath=outputFilePath)
                else:
                        print('No images for timelase gif. Exiting.')

        def rpiZero(self):
                currentDay = datetime.datetime.now().day
                self.daysCycle = itertools.cycle(range(3))
                self.imageCycler = itertools.count(1)
                dayCount = next(self.daysCycle)
                dayFolder = 'day{0}/'.format(dayCount)
                self.archiveFolder = self.archiveBaseFolder + dayFolder
                sleepDuration = 5
                prevImgPath = None

                if os.path.exists(self.archiveFolder):
                        print('Existing archive directory, deleting.')
                        shutil.rmtree(self.archiveFolder)

                while True:
                        currentImgPath = self.timelapse(sleepDuration=sleepDuration, currentDay=currentDay, copyToHAServer=True)
                        self.buildTimelapse(imgNum=self.imgNum)

                        if prevImgPath is not None:
                                self.motionCheck(currentImgPath=currentImgPath, prevImgPath=prevImgPath)
                        prevImgPath = currentImgPath


        def motionCheck(self, currentImgPath, prevImgPath):

                # Read image
                currentImg = Image.open(currentImgPath)
                prevImg = Image.open(prevImgPath)

                currentImg_blur = currentImg.filter(ImageFilter.BLUR)
                prevImg_blur = prevImg.filter(ImageFilter.BLUR)

                buffer1 = np.asarray(currentImg_blur)
                print('sum of img1', np.sum(buffer1))
                buffer2 = np.asarray(prevImg_blur)
                print('sum of img2', np.sum(buffer2))
                # Subtract image2 from image1

                buffer3 = buffer1 - buffer2
                movementValue = np.sum(buffer3)/(buffer1.size)

                client = paho.Client("client-003")
                brokerIP = "10.0.0.19"
                client.connect(brokerIP)
                now = datetime.datetime.now()
                client.publish("rpiMotionTopic", float(movementValue))
                print('')
                print('Motion value:', movementValue)
                print('')


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
                self.imgNum = next(self.imageCycler)

                archiveImage = 'image{0}.jpg'.format(self.imgNum)
                archivePath = self.archiveFolder + archiveImage
                # shutil.copy(currentImagePath, archiveFolder)
                # Create the directory if it doesnt exist
                os.makedirs(self.archiveFolder, exist_ok=True)
                shutil.copy(currentImagePath, archivePath)
                print('Archived image:{}'.format(archivePath))

                if copyToHAServer is True:
                        # self.copyToHAServer(currentImagePath=currentImagePath)
                        inputFilePath = '~/webcamImages/currentImage.jpg'
                        outputFilePath = 'homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/rpi_zero.jpg'
                        self.copyToHAServer(inputFilePath=currentImagePath, outputFilePath=outputFilePath)


                # Sleep delay for next image
                print('Sleeping for {} seconds.'.format(sleepDuration))
                time.sleep(sleepDuration)
                print('')
                return archivePath

if __name__ == '__main__':
        webcam = webcam_timelapse()
        webcam.start()
        exit(0)


