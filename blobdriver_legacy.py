# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, pyb

pin = pyb.Pin("P0", pyb.Pin.OUT_OD)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

threshold = (13, 78, 14, 73, -9, 55)
pinState = False
MIN_AREA = 100

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
    blobs = img.find_blobs([threshold], areaThreshold=5000, merge=True) # detect blobs (red ball)
    newPinState = False
    for blob in blobs:
        img.draw_rectangle(blob.rect(), color=(0,0,255))
        x,y,w,h = blob.rect()
        if w*h >= MIN_AREA:
            newPinState = True
            break
    pinState = newPinState # update pin state if at least one blob satisfies condition
    if pinState:
        pin.high()
    else:
        pin.low()
