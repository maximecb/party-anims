#!/usr/bin/env python3

import time
import math
import random
from threading import Thread
import aubio
import numpy as np
import sounddevice as sd
import cv2






def audio_thread():
    """
    Beat detection thread
    """

    samplerate = 44100
    win_s = 1024        # fft size
    hop_s = win_s // 2  # hop size

    a_tempo = aubio.tempo("default", win_s, hop_s, samplerate)

    stream = sd.InputStream(samplerate=samplerate, blocksize=400, channels=1, dtype=np.float32, latency='low')
    stream.start()

    beat_no = 0
    loud_vals = []

    while True:
        samples, overflowed = stream.read(hop_s)
        samples = samples.squeeze()
        loudness = np.std(samples)
        loud_vals.append(loudness)
        print(loudness)

        if (len(loud_vals) > 500):
            loud_vals.pop(0)

        # Loudness threshold for beat detection
        # Stops beats when the music stops
        if max(loud_vals[-10:]) < 0.05:
            beat = False
        else:
            # Note: we can call o.get_last_s() to get the sample where the beat occurred
            beat = a_tempo(samples)


        # TODO:
        # Act on the beat


        if beat:
            print('|' * 40)
            beat_no += 1
        else:
            print()

    stream.end()

thread = Thread(target = audio_thread)
thread.start()
#thread.join()









class Anim:
    """
    Base class for animations
    """

    def __init__(self):
        pass

    # Reset state, used when switching animations
    def restart(self):
        pass

    def beat(self):
        pass

    def render(self, fb, frame_idx, t):
        raise NotImplementedError

class MerryChristmas(Anim):
    def __init__(self):
        pass

    def render(self, fb, frame_idx, t):
        pass









def draw_text(width, height):
    img = np.zeros((height, width, 3), dtype=np.uint8)

    font.putText(img,
        text='Merry Christmas',
        org=(240, 300),
        fontHeight=250,
        color=(0, 0, 255),
        thickness=-1,
        line_type=cv2.LINE_AA,
        bottomLeftOrigin=False,
    )

    return img.astype(np.float32) / 255

def draw_noise_line(img):
    p1 = np.random.randint(low=(0, 0), high=(width, height), size=2, dtype=int)
    p2 = np.random.randint(low=(0, 0), high=(width, height), size=2, dtype=int)

    cv2.line(
        img,
        p1,
        p2,
        color=(0, 0, 0),
        lineType=cv2.LINE_AA,
        thickness=1
    )







# Load a custom font
font = cv2.freetype.createFreeType2()
font.loadFontData(fontFileName='ferrum.otf', id=0)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)

# Make window fullscreen
#cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 1080p resolution, 16:9 aspect ration, like the projector
width = 1920
height = 1080

# Frame buffer
# In floating point format so we can fade out easily
fb = np.zeros((height, width, 3), dtype=np.float32)









text = draw_text(width, height)
print(text.dtype)
fb += text
















while True:

    for i in range(10):
        draw_noise_line(fb)

    fb *= 0.999
    # Show the current frame
    cv2.imshow('image', fb) 

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  







cv2.destroyAllWindows()












