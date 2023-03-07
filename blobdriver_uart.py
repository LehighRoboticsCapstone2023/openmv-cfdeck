# Untitled - By: jiawei - Thu Feb 23 2023

import math
import sensor, image, time, pyb
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()
uart = UART(1, 115200, timeout_char=100, parity=None)

threshold = (13, 78, 14, 73, -9, 55)
MIN_AREA = 100

while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())

    blobs = img.find_blobs([threshold], areaThreshold=5000, merge=True) # detect blobs (red ball)
    maxBlobArea = 0
    for blob in blobs:
        img.draw_rectangle(blob.rect(), color=(0,0,255))
        x,y,w,h = blob.rect()
        area = w*h
        if (area >= MIN_AREA) and (area > maxBlobArea):
            maxBlobArea = area

    speed = int(255 / math.sqrt(maxBlobArea)) if (maxBlobArea > 0) else 0
    print(speed)
    speed_bytes = speed.to_bytes(1, 'little')

    msg = bytearray(8)
    msg[0] = 0x45
    msg[1] = 1
    msg[2] = speed
    uart.write(msg)
    time.sleep(0.1)
