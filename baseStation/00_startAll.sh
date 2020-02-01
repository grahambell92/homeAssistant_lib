
chmod 775 ./00_startMe.sh
./00_startMe.sh

## start the rpi_zero satellite

#ssh pi@10.0.0.20 'bash -s' < /home/homeassistant/homeAssistant_lib/remoteCamera/00_startMe.sh
ssh pi@192.168.0.56 'bash -s' < /home/homeassistant/homeAssistant_lib/remoteCamera/00_startMe.sh
exit
