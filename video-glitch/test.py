#!/usr/bin/env python3

import time
import random
import math
import cv2  
import numpy as np

# Pad the image into a 16:9 aspect ratio, so we get a back background
def pad_frame(img):
    # Input size is: (576, 720, 3)
    # For 16:9, we want 1024 * 576
    #print(img.shape)
    img = np.pad(img, ((0, 0), (152, 152), (0, 0)))
    #print(img.shape)
    return img

# TODO: we should randomly save previous frames...
# We can keep a list of 1000 old frames, push new frames at the end

# Then random probability of redrawing old frame...?
# Also digital update effect?

vid = cv2.VideoCapture(0) 

cv2.namedWindow("image", cv2.WINDOW_NORMAL)
#cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

max_old_frames = 200
old_frames = []

# TODO: make glitch probabiliy oscillate with sine wave?


# We should maintain a current frame and update rectangles with random probability?

# Frame size is 576, 720
# Both are divisible by 16

# Read the first frame
_, cur_frame = vid.read()




while True: 
    # Read a single frame      
    ret, input_frame = vid.read() 

    # With a random probability, save an old frame
    if random.random() < 1 / 50 and input_frame.any():
        old_frames.append(input_frame)
        if len(old_frames) > max_old_frames:
            old_frames = old_frames[1:]
        print(len(old_frames))

        # TODO: should we show old frame longer? for 2 or 3 frames?
        frame = random.choice(old_frames)




    for j in range(0, 16):
        ystep = input_frame.shape[0] // 16
        ymin = j * ystep
        ymax = ymin + ystep

        for i in range(0, 16):
            xstep = input_frame.shape[1] // 16
            xmin = i * xstep
            xmax = xmin + xstep

            if random.random() < 0.10:
                cur_frame[ymin:ymax, xmin:xmax] = input_frame[ymin:ymax, xmin:xmax]



    if random.random() < 1 / 100 and len(old_frames) > 0:
        old_frame = random.choice(old_frames)
        cur_frame = old_frame.copy()




    # Show the current frame
    cv2.imshow('image', pad_frame(cur_frame)) 

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
vid.release() 
cv2.destroyAllWindows()
