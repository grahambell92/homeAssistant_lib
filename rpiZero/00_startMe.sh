
cd /home/pi/homeAssistant_lib/rpiZero/

# Disable the hdmi output to conserve power.
/opt/vc/bin/tvservice -o

tmux kill-server

tmux new-session -d -s webcam 'python3 01_run_rpiZero_webcamTimelapse.py' &
tmux new-session -d -s rpi_zero_mqtt 'python3 02_mqtt_alivePublish.py'
