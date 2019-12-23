
chmod 775 ./00_startTmuxHomeAssistant.sh
./00_startMe.sh

# Ensure no tmux scripts/sessions are running
tmux kill-server

# AS1231333
## start the rpi_zero satellite
#tmux new-session -d -s rpi_zero_satellite './start_rpiZeroSatellite_0.sh' &
