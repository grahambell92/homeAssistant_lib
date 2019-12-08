
# Ensure scripts not started on any system
# start home assistnat
# start the mqtt server
# start the rpi_zero satellite
# start puller script to pull images from satellite

# Ensure no tmux scripts/sessions are running
tmux kill-server
chmod 775 ./homeAssistant_local/startHomeAssistant.sh
# start the main home assistant sever
tmux new-session -d -s homeAssistant './homeAssistant_local/00_startTmuxHomeAssistant.sh' & #
# start the mqtt publisher (local)
tmux new-session -d -s mqtt 'python3 ./homeAssistant_local/03_example_publisher.py' &

## start the rpi_zero satellite
#tmux new-session -d -s rpi_zero_satellite './start_rpiZeroSatellite_0.sh' &
