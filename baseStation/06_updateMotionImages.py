
import os
import itertools
import subprocess
import time
import shutil

wwwFolder = '/home/pi/homeassistant/www/'
avenueGallery = wwwFolder + 'avenueGallery/'
yardGallery = wwwFolder + 'yardGallery/'

destinations = [avenueGallery, yardGallery]

# Delete the galleries first.
for destination in destinations:
    shutil.rmtree(destination)

currentImgFilenames = [
    'remoteCam0_currentImage_LQ', # .jpg
    'remoteCam1_currentImage_LQ', # '.jpg
]


countCycler = itertools.cycle(range(10))
while True:
    count = next(countCycler)
    for currentImgFilename, destination in zip(currentImgFilenames, destinations):
        os.makedirs(destination, exist_ok=True)
        inputFilePath = wwwFolder + currentImgFilename + '.jpg'
        outputFilePath = destination + currentImgFilename + str(count) + '.jpg'
        command = ' '.join(['cp', inputFilePath, outputFilePath])
        correct = subprocess.run(command, shell=True)
        print('Moved:', inputFilePath)
        print('To:', outputFilePath)
        print()
    time.sleep(90)