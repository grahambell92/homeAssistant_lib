#!/bin/bash
cd /home/pi/homeAssistant_lib/remoteCamera/

# Disable the hdmi output to conserve power.
/opt/vc/bin/tvservice -o

#python3 02_run_rpiZero_imgAcquirer.py &
#python3 03_mqtt_alivePublish.py &
# Use the full path to start tmux
#/usr/bin/tmux set remain-on-exit on
/usr/bin/tmux kill-server
echo 'Killed server'
echo 'Waiting 5 seconds to release camera...'
sleep 5
#/usr/bin/tmux new-session -d -s camera '/usr/bin/python3 02_run_rpiZero_imgAcquirer.py'
/usr/bin/tmux new-session -d -s camera '/usr/bin/python3 05_run_surveilanceCamera.py'

echo 'Started img aquisition'
/usr/bin/tmux new-session -d -s mqtt '/usr/bin/python3 03_mqtt_alivePublish.py'
echo 'Started mqtt publisher'

#echo 'Started running log checker' # er
#/usr/bin/tmux new-session -d -s rpiOnline '/usr/bin/python3 06_run_piOnlineChecker.py'

# tmux new-session -d -s gifBuilder 'python3 04_run_rpiZero_buildTimelapseGif.py' &
