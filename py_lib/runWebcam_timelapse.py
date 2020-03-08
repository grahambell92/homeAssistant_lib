# This file is for

import subprocess
import datetime
import itertools
import os
import shutil
import time
import imageio
from PIL import Image, ImageFilter, ImageChops
import numpy as np
import paho.mqtt.client as paho
import glob
import math

class webcam_timelapse():
        def __init__(self, archiveBaseFolder='/home/pi/webcamImages/',):
                self.archiveBaseFolder = archiveBaseFolder
                self.archiveFolder = self.archiveBaseFolder + 'rollingImages/'
                self.currentImagePath = self.archiveBaseFolder + 'currentImage.jpg'
                self.currentGifPath = self.archiveBaseFolder + 'currentSeq.gif'

        def fireCamera(self, filePath):
            print('Firing camera...')
            # correct = subprocess.run(['fswebcam', '-r 640x480', '--quiet', filePath])
            # correct = subprocess.run('fswebcam -r 640x480 --quiet --jpeg 50 {}'.format(filePath), shell=True)
            # Use the rasperry pi noIR camera instead
            correct = subprocess.run('raspistill -o {0} -q 3 -t 1500'.format(filePath), shell=True)
            print('Done.')

        def scpToRemote(self, inputFilePath, outputFilePath):
                # shouldn't need the passwd because of ssh key installed.
                print('Trying to copy img to remote...')
                print('SCP from:', inputFilePath)
                print('SCP to:', outputFilePath)
                print()
                # inputFilePath = '~/webcamImages/currentImage.jpg'
                # outputFilePath = 'homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/'
                # command = 'scp ~/webcamImages/currentImage.jpg homeassistant@10.0.0.19:/home/homeassistant/.homeassistant/www/'
                command = ' '.join(['scp', inputFilePath, outputFilePath])
                correct = subprocess.run(command, shell=True)
                print('Done.')

        def copyTowwwFolder(self, currentImagePath):

                # Copy to the www folder for the HomeAssistant Server
                wwwFolder = '/home/homeassistant/.homeassistant/www/'
                os.makedirs(wwwFolder, exist_ok=True)
                shutil.copy(currentImagePath, wwwFolder)
                print('Copied to HA local folder:{}'.format(wwwFolder))


        def buildTimelapseGif(self, numImgs=10, remoteCopyLocation=None, fps=None,):
                # Make a gif of the most recent images
                imgPaths = glob.glob(self.archiveFolder + '*.jpg')
                imgPaths.sort(key=os.path.getmtime)
                print(imgPaths)

                gifimages = []
                for index, imgPath in enumerate(imgPaths[-numImgs:]):
                        try:
                                gifimages.append(imageio.imread(imgPath))
                                print('#', index, 'Appended:', imgPath)
                        except:
                                print('#', index, 'Unable to read:', imgPath)

                if False:
                        if len(imgPaths) > 0:
                                # Build the input file list

                                inputFileCommand = ' -i '.join(imgPaths[:3])

                                # use this input from:
                                # https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality
                                # ffmpeg -i input.mp4 -vf "fps=3:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
                                # ffmpeg -y -i /home/pi/webcamImages/rollingImages/image0.jpg -filter_complex "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse" FancyStickAround.gif
                                gifCommand = ['ffmpeg', '-y', '-r 3', '-i', inputFileCommand,
                                              '-filter_complex "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse"',
                                              self.currentGifPath
                                              ]
                                gifCommand = " ".join(gifCommand)
                                print(gifCommand)
                                exit(0)
                                correct = subprocess.run(gifCommand, shell=True)

                                # Move the image via secure copy (scp) to the home assistant www folder on the main rpi.
                                if remoteCopyLocation is not None:
                                        print('Copying to remote HA www folder...')
                                        self.scpToRemote(inputFilePath=self.currentGifPath, outputFilePath=remoteCopyLocation)
                                        print('Done.')


                if len(gifimages) > 0:
                        imageio.mimsave(self.currentGifPath, gifimages, fps=fps, subrectangles=True)
                        print('Saving current gif:', self.currentGifPath)

                        # Compress using gifsicle
                        if True:
                            gifCommand = ['gifsicle -i {0} --optimize=3 --colors 64 -o {0}'.format(self.currentGifPath)]
                            correct = subprocess.run(gifCommand, shell=True)

                        # Compress gif using ffmpeg.
                        if False:
                                gifCommand = ['ffmpeg', '-y', '-i', self.currentGifPath,
                                              '-filter_complex "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse"',
                                              self.currentGifPath
                                              ]
                                gifCommand = " ".join(gifCommand)
                                print(gifCommand)
                                correct = subprocess.run(gifCommand, shell=True)

                        # Move the image via secure copy (scp) to the home assistant www folder on the main rpi.
                        if remoteCopyLocation is not None:
                                print('Copying to remote HA www folder...')
                                self.scpToRemote(inputFilePath=self.currentGifPath, outputFilePath=remoteCopyLocation)
                                print('Done.')

                else:
                        print('No images for timelapse gif. Exiting.')

        def image_entropy(self, img):
                """calculate the entropy of an image"""
                # this could be made more efficient using numpy
                histogram = img.histogram()
                histogram_length = sum(histogram)
                samples_probability = [float(h) / histogram_length for h in histogram]
                return -sum([p * math.log(p, 2) for p in samples_probability if p != 0])

        def motionCheck(self, currentImgPath, prevImgPath, remoteCopyPath=None,
                        mqttBrokerIP="192.168.0.55",
                        motionThreshold=5.5,
                        mqttMotionPublishTopic='motion',
                        mqttMotionClient='runWebcam_timelapse.py'):

                # Read image
                currentImg = Image.open(currentImgPath)
                prevImg = Image.open(prevImgPath)

                imgDiff = ImageChops.difference(currentImg, prevImg)
                imgEntropy = self.image_entropy(img=imgDiff)

                try:
                        client = paho.Client(mqttMotionClient)
                        client.connect(mqttBrokerIP)
                        client.publish(mqttMotionPublishTopic, '{:.2f}'.format(imgEntropy))
                        print('')
                        print('Motion value:', imgEntropy)
                        print('')
                except:
                        print('MQTT publish failed. Passing over.')

                if imgEntropy > motionThreshold and remoteCopyPath is not None:
                        print('Motion detected! Copying to remote.')
                        self.scpToRemote(currentImgPath, outputFilePath=remoteCopyPath)


        def takeAndArchive(self, imgArchiveNum, sleepDuration=120, remoteCopyLocation=None):
                # Take an image for the current image
                self.fireCamera(filePath=self.currentImagePath)

                # Archive the image
                archiveImage = 'image{0}.jpg'.format(imgArchiveNum)
                self.currentArchivePath = self.archiveFolder + archiveImage
                # Create the directory if it doesnt exist
                os.makedirs(self.archiveFolder, exist_ok=True)
                shutil.copy(self.currentImagePath, self.currentArchivePath)
                print('Archived image:{}'.format(self.currentArchivePath))

                # Move the image via secure copy (scp) to the home assistant www folder on the main rpi.
                if remoteCopyLocation is not None:
                        self.scpToRemote(inputFilePath=self.currentImagePath, outputFilePath=remoteCopyLocation)

                # Sleep delay for next image
                print('Sleeping for {} seconds.'.format(sleepDuration))
                time.sleep(sleepDuration)
                print('')
                return

if __name__ == '__main__':
        webcam = webcam_timelapse()
        webcam.start()
        exit(0)


