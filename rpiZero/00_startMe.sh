
tmux kill-session
#00_start_Tmux_rpiZero_webcamTimelapse.sh &
cd /home/pi/homeAssistant_lib/rpiZero/
tmux new-session -d -s webcam 'python3 01_run_rpiZero_webcamTimelapse.py'
tmux new-session -d -s rpi_zero_mqtt 'python3 02_mqtt_alivePublish.py'