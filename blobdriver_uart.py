# Untitled - By: jiawei - Thu Feb 23 2023

import math
import sensor, image, time, pyb
from pyb import UART

# init camera sensor
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

# init UART and timer
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
    for blob in blobs: # find largest blob
        img.draw_rectangle(blob.rect(), color=(0,0,255))
        x,y,w,h = blob.rect()
        area = w*h
        if (area >= MIN_AREA) and (area > maxBlobArea):
            maxBlobArea = area

    speed = int(255 / math.sqrt(maxBlobArea)) if (maxBlobArea > 0) else 0 # stupid speed formula (Z thrust)
    print(speed)
    #speed_bytes = speed.to_bytes(1, 'little')

    msg = bytearray(8)
    msg[0] = 0x69           # start bytes (the other end must synchronize to this pattern)
    msg[1] = 0x69
    msg[2] = 1              # "command" (arbitrary for now) - set Z velocity
    msg[3] = speed          # write speed as one byte (quantized 0-255)
    uart.write(msg)         # send 8 byte message
    time.sleep(0.1)         # 100ms delay
