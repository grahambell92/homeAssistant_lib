# tmux new-session -d -s webcam 'python3 runTimeLapse.py' &

ssh pi@10.0.0.20
cd ~/homeLib/rpiZero
tmux kill-session

tmux new-session -d -s rpi_zero_satellite '00_start_Tmux_rpiZero_webcamTimelapse.sh'
