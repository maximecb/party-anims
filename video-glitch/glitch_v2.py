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

vid = cv2.VideoCapture(0) 

cv2.namedWindow("image", cv2.WINDOW_NORMAL)

# Make window fullscreen
cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)




# Array of saved clips
saved_clips = []

# Clip currently being recorded
frames_to_record = 0
current_clip = None

# Clip being played back
playback_clip = None

# Frame size is 576, 720
# Both are divisible by 16
# Read the first frame
_, cur_frame = vid.read()




while True: 
    # Read a single frame      
    ret, input_frame = vid.read() 
    #print(input_frame.shape)

    num_rows, num_cols, _ = input_frame.shape
    #print(num_rows)

    # Time lag
    #time.sleep(random.uniform(0.01, 0.1))

    # With a small probability, record a new clip
    if current_clip == None and random.random() < 1/300:
        frames_to_record = random.randint(1, 30)
        current_clip = []
        print('recording clip, num_frames={}'.format(frames_to_record))

    # If we are currently recording a clip
    if frames_to_record > 0:
        current_clip.append(input_frame)
        frames_to_record -= 1
        if frames_to_record == 0:
            assert len(current_clip) > 0
            saved_clips.append(current_clip)
            current_clip = None
            print('done recording clip')
        if len(saved_clips) > 200:
            saved_clips.pop(0)

    # If we are currently playing a clip
    if playback_clip != None:
        input_frame = playback_clip.pop(0)
        if len(playback_clip) == 0:
            playback_clip = None

    # With a small probability, playback a saved clip
    if playback_clip == None and len(saved_clips) > 0 and random.random() < 1/150:
        playback_clip = random.choice(saved_clips).copy()
        assert len(playback_clip) > 0
        print('playing clip, len={}'.format(len(playback_clip)))


    # For each row
    for j in range(0, num_rows):

        if random.random() < 0.85:
            #row_shift = random.randint(0, 5)
            #v_shift = random.randint(-2, 2)
            row_shift=0
            v_shift=0
            in_j = min(max(j + v_shift, 0), num_rows - 1)
            cur_frame[j, row_shift:] = input_frame[in_j, 0:(num_cols - row_shift)]





    # Show the current frame
    cv2.imshow('image', pad_frame(cur_frame)) 

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
vid.release() 
cv2.destroyAllWindows()
