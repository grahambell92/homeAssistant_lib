
tmux kill-session
tmux new-session -d -s rpi_zero_webcam '00_start_Tmux_rpiZero_webcamTimelapse.sh'
tmux new-session -d -s rpi_zero_mqtt 'python3 02_mqtt_alivePublish.py'