# openmv-cfdeck
A suite of OpenMV programs and helper scripts, for use as a Crazyflie deck.

## Instructions

For now, copy the file `blobdriver.py` to the OpenMV deck's storage, and rename it to `main.py`.

Ensure `P0` on the OpenMV is connected to `PB8` on the Crazyflie, and that the [relevant firmware](https://github.com/LehighRoboticsCapstone2023/crazyflie-firmware) is uploaded. You are advised to ground the devices relatively, using the `GND` pins.
