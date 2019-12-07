
# Ensure scripts not started on any system
# start home assistnat
# start the mqtt server
# start the rpi_zero satellite
# start puller script to pull images from satellite

# Ensure no tmux scripts/sessions are running
tmux kill-server
# start the main home assistant sever
tmux new-session -d -s homeAssistant './startHomeAssistant.sh' & #
# start the mqtt publisher (local)
tmux new-session -d -s mqtt 'python3 example_publisher.py' &

## start the rpi_zero satellite
#tmux new-session -d -s rpi_zero_satellite './start_rpiZeroSatellite_0.sh' &
