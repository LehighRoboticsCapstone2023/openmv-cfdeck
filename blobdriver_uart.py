# blobdriver_uart.py
# Author: Michael Fitzgerald (mtf323@lehigh.edu)
# Year: 2023

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
uart = UART(3, 115200, timeout_char=100, parity=None)

threshold = (37, 73, 22, 81, 18, 64)
MIN_AREA = 100

# OpenMV OV7725 sensor focal length: 311px (both axes)

FOCAL_LEN = 311 # in pixels
BALLOON_WIDTH = 0.3 # in meters

def calc_dist(pix_width):
    return BALLOON_WIDTH * FOCAL_LEN / pix_width

while(True):
    clock.tick()
    img = sensor.snapshot()
    print(clock.fps())

    blobs = img.find_blobs([threshold], areaThreshold=5000, merge=True) # detect blobs (red ball)
    (maxBlobX, maxBlobY, maxBlobW, maxBlobH) = (0,0,0,0)
    maxBlobArea = 0
    isActive = False
    for blob in blobs: # find largest blob
        x,y,w,h = blob.rect()
        area = w*h
        if area >= MIN_AREA:
            img.draw_rectangle(blob.rect(), color=(0,0,255))
            if area > maxBlobArea:
                (maxBlobX, maxBlobY, maxBlobW, maxBlobH) = (x,y,w,h)
                maxBlobArea = area

    if (maxBlobArea > 0):
        isActive = True
    blobX = (2*maxBlobX + maxBlobW) / 2
    blobY = (2*maxBlobY + maxBlobH) / 2
    x = int((blobX - 160) * 127 / 160)
    y = int((blobY - 120) * 127 / 120)
    blobRadius = math.sqrt(maxBlobArea / math.pi)
    z = int(10*calc_dist(2 * blobRadius)) if (blobRadius > 0) else 0 # distance in 1/10 meters
    if z == 0:
        (x,y) = (0,0)
    #print(speed)
    #speed_bytes = speed.to_bytes(1, 'little')

    print(x,y,z)

    msg = bytearray(8)
    msg[0] = 0x69           # start bytes (the other end must synchronize to this pattern)
    msg[1] = 0x69
    msg[2] = 1              # "command" (arbitrary for now) - set Z velocity
    msg[3] = isActive
    msg[4] = x
    msg[5] = y
    msg[6] = z
    #print(msg)
    uart.write(msg)         # send 8 byte message
    time.sleep(0.1)         # 100ms delay
