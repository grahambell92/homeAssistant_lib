import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
outPin = 13
GPIO.setup(outPin, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
while True:  # Run forever
    print('Lamp is on...')
    GPIO.output(outPin, GPIO.HIGH)  # Turn on
    sleep(100)  # Sleep for 1 second
    print('Lamp is off...')
    GPIO.output(outPin, GPIO.LOW)  # Turn off
    sleep(1)  # Sleep for 1 second