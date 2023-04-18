# openmv-cfdeck
A suite of OpenMV programs and helper scripts, for use as a Crazyflie deck.

## Instructions

Depending on your use case:
- For the modern UART system, copy the file `blobdriver_uart.py` to the OpenMV deck's storage, and rename it to `main.py`.
- For the legacy GPIO-only system, copy the file `blobdriver_legacy.py` to the OpenMV deck's storage, and rename it to `main.py`.

Please install the [relevant firmware](https://github.com/LehighRoboticsCapstone2023/crazyflie-firmware). Then connect `P4` on the OpenMV to `PC11` on the Crazyflie (and ensure common ground via `GND`).
