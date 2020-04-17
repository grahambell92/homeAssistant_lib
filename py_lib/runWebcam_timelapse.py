# This file is for

import subprocess
from datetime import datetime
import itertools
import os
import shutil
import io
import time
import imageio
from PIL import Image, ImageFilter, ImageChops
import numpy as np
import paho.mqtt.client as paho
import glob
import math
import picamera
from picamera.array import PiRGBArray
import imutils
import cv2

class webcam_timelapse():
    def __init__(self, archiveBaseFolder='/home/pi/webcamImages/', cameraName='default', cameraNumber=0):
        self.archiveBaseFolder = archiveBaseFolder
        os.makedirs(self.archiveBaseFolder, exist_ok=True)
        self.archiveFolder = self.archiveBaseFolder + 'archiveImages/'
        self.currentImagePath_HQ = self.archiveBaseFolder + 'currentImage_HQ.jpg'
        self.currentImagePath_LQ = self.archiveBaseFolder + 'currentImage_LQ.jpg'
        self.currentGifPath = self.archiveBaseFolder + 'currentSeq.gif'

        self.cameraName = cameraName
        self.cameraNumber = cameraNumber
        self.daysToKeep = 3
        self.liveViewQuality = 20

    def fireCamera(self, filePath, quality=3, flipVert=False, flipHorz=False):
        print('Firing camera...')
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            # Camera warm-up time
            time.sleep(2)
            camera.vflip = flipVert
            camera.hflip = flipHorz
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            camera.capture(filePath, format='jpeg', quality=quality)
            camera.stop_preview()

        if False:
            # correct = subprocess.run(['fswebcam', '-r 640x480', '--quiet', filePath])
            # correct = subprocess.run('fswebcam -r 640x480 --quiet --jpeg 50 {}'.format(filePath), shell=True)
            # Use the rasperry pi noIR camera instead

            if flipVert is True:
                flipVert = '-vf'
            else:
                flipVert = ''

            if flipHorz is True:
                flipHorz = '-hf'
            else:
                flipHorz = ''

            command = 'raspistill -o {0} -q {1} -t 1500 {2} {3}'.format(filePath, quality, flipVert, flipHorz)
            correct = subprocess.run(command, shell=True)

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
        import os.path
        outputDest, outputFile = os.path.split(outputFilePath)
        remoteHost, outputFolder = outputDest.split(':')

        # ssh remote-host 'mkdir -p foo/bar/qux'
        # remote_host =
        command = ' '.join(['ssh', remoteHost, "'mkdir -p {:}'".format(outputFolder)])
        correct = subprocess.run(command, shell=True)

        command = ' '.join(['scp', inputFilePath, outputFilePath])
        correct = subprocess.run(command, shell=True)

        # command = ' '.join(['rsync -a --compress', inputFilePath, outputFilePath])
        # correct = subprocess.run(command, shell=True)

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

        if False:
            gifimages = []
            for index, imgPath in enumerate(imgPaths[-numImgs:]):
                try:
                    gifimages.append(imageio.imread(imgPath))
                    print('#', index, 'Appended:', imgPath)
                except:
                    print('#', index, 'Unable to read:', imgPath)

        if len(imgPaths) > 0:
            with imageio.get_writer(self.currentGifPath, mode='I') as writer:
                for index, imgPath in enumerate(imgPaths[-numImgs:]):
                    image = imageio.imread(imgPath)
                    print('Writing:', imgPath)
                    writer.append_data(image)

            if False:
                imageio.mimsave(self.currentGifPath, gifimages, fps=fps, subrectangles=True)
                print('Saving current gif:', self.currentGifPath)

            # Compress using gifsicle
            if False:
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

    def archiveDayFolderString(self):
        now = datetime.now()  # current date and time
        # date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        archiveDayFolder = now.strftime("%j_%d%B%Y")
        return archiveDayFolder


    def takeCurrentImage(self,
                         imagePath=None,
                         quality=3,
                         flipVert=False,
                         flipHorz=False):
        # Take an image for the current image
        if imagePath is None:
            imagePath = self.currentImagePath_HQ

        self.fireCamera(filePath=imagePath,
                        quality=quality,
                        flipVert=flipVert,
                        flipHorz=flipHorz
                        )

    def archiveImage(self,
                     currentImagePath_HQ,
                     remoteCopyLocation_LQ=None,
                     remoteCopyLocation_HQ=None,
                     remoteArchiveFolder=None,
                     ):
        # day of year, date in human readable form/camera/time_camera.png
        # The format is: 312_24April2020/01_avenue/12-23-21_avenue.png
        # The format is: 313_24April2020/02_yard/12-23-21_yard.png

        now = datetime.now()  # current date and time

        # date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        archiveDayFolder = now.strftime("%j_%d%B%Y")
        cameraFolder = ('{0:02d}_{1}').format(self.cameraNumber, self.cameraName)
        archiveFile = now.strftime('%H-%M-%S.jpg')
        relativeArchiveFolder = archiveDayFolder + '/' + cameraFolder + '/'
        relativeArchivePath = relativeArchiveFolder + archiveFile
        print('New Relative archive path:', relativeArchivePath)

        # self.currentArchivePath = self.archiveFolder + archiveImage
        self.currentArchivePath = self.archiveFolder + relativeArchivePath
        print('Archive location:', self.currentArchivePath)

        # Make sure the relativeArchiveFolder exists
        currentArchiveFolder = self.archiveFolder + relativeArchiveFolder
        os.makedirs(currentArchiveFolder, exist_ok=True)

        # Create the directory if it doesnt exist
        os.makedirs(self.archiveFolder, exist_ok=True)
        shutil.copy(self.currentImagePath_HQ, self.currentArchivePath)
        print('Archived image:{}'.format(self.currentArchivePath))

        # Move the image via secure copy (scp) to the home assistant www folder on the main rpi.
        if remoteCopyLocation_LQ is not None:
            # Compress the image for the live view
            image = Image.open(self.currentImagePath_HQ)
            image.save(self.currentImagePath_LQ,
                       quality=self.liveViewQuality)  # , optimize=True) # Optimise uses a lot of processing power apparently.
            self.scpToRemote(inputFilePath=self.currentImagePath_LQ, outputFilePath=remoteCopyLocation_LQ)

        if remoteCopyLocation_HQ is not None:
            self.scpToRemote(inputFilePath=self.currentImagePath_HQ, outputFilePath=remoteCopyLocation_HQ)

        if remoteArchiveFolder is not None:
            # Also put the image into archive storage on the basestation as well.
            remoteArchivePath = remoteArchiveFolder + relativeArchivePath
            self.scpToRemote(inputFilePath=self.currentImagePath_HQ, outputFilePath=remoteArchivePath)

    def takeAndArchive(self,
                       sleepDuration=120,
                       remoteCopyLocation_LQ=None,
                       remoteCopyLocation_HQ=None,
                       remoteArchiveFolder=None,
                       ):

        # Take an image for the current image
        self.fireCamera(filePath=self.currentImagePath_HQ,
                        quality=quality,
                        flipVert=flipVert,
                        flipHorz=flipHorz
                        )

        self.archiveImage(
            currentImagePath_HQ=self.currentImagePath_HQ,
            remoteCopyLocation_LQ=remoteCopyLocation_LQ,
            remoteCopyLocation_HQ=remoteCopyLocation_HQ,
            remoteArchiveFolder=remoteArchiveFolder,
        )

        time.sleep(sleepDuration)


    def removeOldDayOfYearFolders(self):
        now = datetime.now()  # current date and time
        dayOfYearToday = now.strftime("%j")
        # Day folder locaions
        # Get folders in the archive store
        for folder in glob.glob(self.archiveFolder + "*/"):
            # First 3 chars of folder correspond to the day of year
            print('Examining folder:', folder)
            subFolder = folder.replace(self.archiveFolder, "") # Remove the full path
            folder_dayOfYear = int(subFolder[:3])
            print('doy', folder_dayOfYear)
            # Last if is incase it's at the end of the year and new year.
            try:
                if folder_dayOfYear + self.daysToKeep < int(dayOfYearToday) and int(dayOfYearToday) > self.daysToKeep:
                    print('Deleting folder:', folder)
                    shutil.rmtree(folder)
                else: print('Retaining folder:', folder)
            except:
                print('Unable to parse or delete existing day of year archive folder:', folder)

    def motionSurveilance(self,
                          remoteCopyLocation_LQ=None,
                          remoteCopyLocation_HQ=None,
                          remoteArchiveFolder=None,
                          flipVert=False,
                          flipHorz=False,
                          timelapseInterval=15,
                          removeOldData=False,
                          cameraFPS=24,
                          cameraResolution=(1024, 768),
                          delayBetweenMotionEvents=3.0,
                          minFramesToTrigMotion=3,
                          motionThreshold=2,
                          minMotionArea=5000):

        if removeOldData is True:
            self.removeOldDayOfYearFolders()

        # initialize the camera and grab a reference to the raw camera capture
        camera = picamera.PiCamera()
        camera.framerate = cameraFPS
        camera.vflip = flipVert
        camera.hflip = flipHorz

        # Create the in-memory stream
        stream = io.BytesIO()
        camera.start_preview()
        time.sleep(2)


        currentMotionImage = 'currentMotion.jpg'
        currentTimelapse = 'currentTimelapse.jpg'

        lastTimeLapseTime = datetime.now()

        # allow the camera to warmup, then initialize the average frame, last
        # uploaded timestamp, and frame motion counter

        print("[INFO] warming up...")
        time.sleep(2.0)

        avg = None
        lastUploaded = datetime.now()
        motionCounter = 0

        while True:
            camera.capture(stream, format='jpeg')
            print('Capturing image')
            # Construct a numpy array from the stream
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            # "Decode" the image from the array, preserving colour
            frame = cv2.imdecode(data, 1)

            timestamp = datetime.now()
            text = "Unoccupied"
            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the average frame is None, initialize it
            if avg is None:
                print("[INFO] starting background model...")
                avg = gray.copy().astype("float")
                # rawCapture.truncate(0)
                continue

            # accumulate the weighted average between the current frame and
            # previous frames, then compute the difference between the current
            # frame and running average
            cv2.accumulateWeighted(src=gray, dst=avg, alpha=0.5)
            frameDelta = cv2.absdiff(src1=gray, src2=cv2.convertScaleAbs(avg))

            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh = cv2.threshold(src=frameDelta, thresh=motionThreshold, maxval=255, type=cv2.THRESH_BINARY)[1]

            thresh = cv2.dilate(thresh, None, iterations=2)
            contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)
            # loop over the contours
            for contour in contours:
                # if the contour is too small, ignore it
                if cv2.contourArea(contour) > minMotionArea:
                    # compute the bounding box for the contour, draw it on the frame,
                    # and update the text
                    (x, y, w, h) = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    text = "Occupied"


            # draw the text and timestamp on the frame
            # camera.annotate_background = picamera.Color('black')
            # camera.annotate_text = datetime.now().strftime('%d-%m-%Y %H:%M:%S\nStatus: {0}'.format(text))

            # ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            timeText = datetime.now().strftime('%d-%m-%Y %H:%M:%S\nStatus: {0}'.format(text))
            cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, timeText, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            # check to see if the room is occupied
            if text == "Occupied":
                # check to see if enough time has passed between uploads
                if (timestamp - lastUploaded).seconds >= delayBetweenMotionEvents:
                    # increment the motion counter
                    motionCounter += 1
                    # check to see if the number of frames with consistent motion is
                    # high enough
                    if motionCounter >= minFramesToTrigMotion:
                        # Here's where you've satisfied the conditions and will post an additional motion image.
                        if True:
                            # Save the image to currentMotion.jpg
                            cv2.imsave(frame, 'currentMotion.jpg')
                            print('Saving motion images...')
                            # Archive the currentMotion.jpg with the _motion suffix to the remote directories.

                            self.archiveImage(
                                currentImagePath_HQ='currentMotion.jpg',
                                remoteCopyLocation_LQ=remoteCopyLocation_LQ.replace('.jpg', '_motion.jpg'),
                                remoteCopyLocation_HQ=remoteCopyLocation_HQ.replace('.jpg', '_motion.jpg'),
                                remoteArchiveFolder=remoteArchiveFolder.replace('.jpg', '_motion.jpg'),
                            )
                            # update the last uploaded timestamp and reset the motion
                            # counter
                            print('Done.')
                            lastUploaded = timestamp
                            motionCounter = 0
            # otherwise, the room is not occupied
            else:
                motionCounter = 0

                # If the elapsed time is past the regular image interval time.
                # Archive the image without the _motion suffix.
                print('time since last timelapse img: ', (datetime.now() - lastTimeLapseTime).seconds)
                if (datetime.now() - lastTimeLapseTime).seconds > timelapseInterval:
                    print('Saving timelapse image.')
                    cv2.imwrite(filename=currentTimelapse, image=frame)
                    self.archiveImage(
                        currentImagePath_HQ=currentTimelapse,
                        remoteCopyLocation_LQ=remoteCopyLocation_LQ,
                        remoteCopyLocation_HQ=remoteCopyLocation_HQ,
                        remoteArchiveFolder=remoteArchiveFolder,
                    )
                    lastTimeLapseTime = datetime.now()
                    print('Done.')

            # check to see if the frames should be displayed to screen
            if False:
                if config["show_video"]:
                    # display the security feed
                    cv2.imshow("Security Feed", frame)
                    key = cv2.waitKey(1) & 0xFF
                    # if the `q` key is pressed, break from the lop
                    if key == ord("q"):
                        break

            # clear the stream in preparation for the next frame
            # rawCapture.truncate(0)

if __name__ == '__main__':
    webcam = webcam_timelapse()
    webcam.start()
    exit(0)


