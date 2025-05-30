# Automation ThorLabs

This repo contains code to control ThorLabs motorized stages using Python.

## How to Use
Run the `initialize_motor()` and `move_motor(x, y)` functions with desired angles. Both motors are running with this code, but they disconnect after every loop or move. It looks like we need to troubleshoot the Raspberry Pi side and adjust its configuration to pinpoint and fix the disconnection issue.
