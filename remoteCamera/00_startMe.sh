
cd /home/pi/homeAssistant_lib/remoteCamera/

# Disable the hdmi output to conserve power.
/opt/vc/bin/tvservice -o

tmux kill-server

tmux new-session -d -s imgAcquirer 'python3 02_run_rpiZero_imgAcquirer.py' &
tmux new-session -d -s rpi_zero_mqtt 'python3 03_mqtt_alivePublish.py' &
tmux new-session -d -s gifBuilder 'python3 04_run_rpiZero_buildTimelapseGif.py' &