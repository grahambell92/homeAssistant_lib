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
/usr/bin/tmux new-session -d -s camera '/usr/bin/python3 02_run_rpiZero_imgAcquirer.py'
echo 'Started img aquisition'
/usr/bin/tmux new-session -d -s mqtt '/usr/bin/python3 03_mqtt_alivePublish.py'
echo 'Started mqtt publisher'

# tmux new-session -d -s gifBuilder 'python3 04_run_rpiZero_buildTimelapseGif.py' &
