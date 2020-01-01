
chmod 775 ./00_startMe.sh
./00_startMe.sh

## start the rpi_zero satellite

ssh pi@10.0.0.20
/home/pi/homeAssistant_lib/rpiZero/00_startMe.sh
#tmux new-session -d -s rpi_zero_satellite './start_rpiZeroSatellite_0.sh' &
