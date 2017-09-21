#!/usr/bin/env bash

python3 debugger.py localhost 7777 &
HEPH_DEBUGGER_PID=$!

python3 okc_messenger.py localhost 7777 &
HEPH_MESSENGER_SERVER_PID=$!

control_c() {
    echo ""
    echo ""
    echo "Ending program..."
    kill ${HEPH_MESSENGER_SERVER_PID}
    echo "Terminated messenger server."
    kill ${HEPH_DEBUGGER_PID}
    echo "Terminated debugger."

    echo "Program exited."
    exit
}

trap control_c SIGINT

while true ; do
   :
done
