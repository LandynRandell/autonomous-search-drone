#!/bin/bash
pkill -9 -f 'build/sitl/bin/arducopter'
pkill -9 -f '/mavproxy.py'
pkill -9 -f 'autotest/sim_vehicle.py'
sleep 1
cd ~/ardupilot/ArduCopter
exec ~/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter --console --map --out 127.0.0.1:14551 --wipe-eeprom