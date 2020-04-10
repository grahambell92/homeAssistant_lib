
import os
import itertools
import subprocess
import time

wwwFolder = '/home/pi/homeassistant/www/'
avenueGallery = wwwFolder + 'avenueGallery/'
yardGallery = wwwFolder + 'yardGallery/'

destinations = [avenueGallery, yardGallery]

currentImgFilenames = [
    'remoteCam0_currentImage_LQ', # .jpg
    'remoteCam1_currentImage_LQ', # '.jpg
]

countCycler = itertools.cycle(itertools.count(10))
while True:
    for currentImgFilename, destination in zip(currentImgFilenames, destinations):
        os.makedirs(destination, exist_ok=True)
        count = next(countCycler)
        inputFilePath = wwwFolder + currentImgFilename
        outputFilePath = avenueGallery + currentImgFilename + str(count) + '.jpg'
        command = ' '.join(['cp', inputFilePath, outputFilePath])
        correct = subprocess.run(command, shell=True)
        print('Moved:', inputFilePath)
        print('To:', outputFilePath)
        print()
    time.sleep(90)