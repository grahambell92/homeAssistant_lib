
# Ensure scripts not started on any system
# start home assistnat
# start the mqtt server
# start the rpi_zero satellite
# start puller script to pull images from satellite

# Ensure no tmux scripts/sessions are running
tmux kill-server
chmod 775 ./00_startTmuxHomeAssistant.sh
chmod 775 ./01_startHomeAssistant.sh
# start the main home assistant sever

# Start the tmux version
tmux new-session -d -s homeAssistant './01_startHomeAssistant.sh'

# start the mqtt publisher (local)
tmux new-session -d -s mqtt 'python3 ./00_serialToMqttTest.py'
