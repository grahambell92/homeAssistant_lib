
chmod 775 ./00_startMe.sh
./00_startMe.sh

## start the rpi_zero satellite

ssh pi@10.0.0.20 ssh 'bash -s' < /home/pi/homeAssistant_lib/rpiZero/00_startMe.sh
exit
