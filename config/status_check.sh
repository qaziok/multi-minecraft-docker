#!/bin/bash

players_sum=0

cancel_shutdown(){
    echo "Cancelling current shutdown"
    sudo shutdown -c
}

enable_shutdown(){
    echo "It's time to schedule a shutdone"
    sudo shutdown +30
}

trap 'cancel_shutdown' ERR

for containerId in $(sudo docker ps -aqf "name=mc-1")
    do
        online_players=$(sudo docker exec $containerId ./health.sh | grep -oP 'online=\K\d+')
        players_sum=$((players_sum+online_players))
    done

if [ "$players_sum" -gt 0 ]; then
    [ -f /run/systemd/shutdown/scheduled ] && cancel_shutdown
else
    [ ! -f /run/systemd/shutdown/scheduled ] && enable_shutdown
fi
