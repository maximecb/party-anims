#!/usr/bin/env python3

import time
import math
import random
from threading import Thread
import numpy as np
import cv2
import socket
import itertools
import sys

class BeatClient:
    def __init__(self, server_addr="192.168.1.211", server_port=7777):
        # Create and bind the local socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 9999))

        # Non-blocking mode
        self.sock.settimeout(0)

        # Send subscribe message to server
        self.sock.sendto(b"sub", (server_addr, server_port))

    def beat_received(self):
        try:
            # Receive a UDP packet
            data, addr = self.sock.recvfrom(1024)
            return True
        except socket.error as e:
            if e.args[0] == socket.EAGAIN:
                # No data available, try again later
                return False
            else:
                # Handle other socket errors
                print(f"Socket error: {e}")

class Anim:
    """
    Base class for animations
    """

    def __init__(self):
        pass

    # Reset state, used when switching animations
    def restart(self):
        pass

    def beat(self, beat_idx, t):
        pass

    def render(self, fb, frame_idx, t):
        raise NotImplementedError




class MerryHS(Anim):
    def __init__(self):
        pass



    def beat(self, fb, beat_idx, t):
        #fb[:] = 0

        if beat_idx % 4 == 0:
            fb += draw_text(
                fb.shape[0],
                fb.shape[1],
                x=240,
                y=300,
                font_size=250,
                text="Merry Christmas"
            )
        elif beat_idx % 4 == 2:
            fb += draw_text(
                fb.shape[0],
                fb.shape[1],
                x=460,
                y=300,
                font_size=250,
                text="Hail Satan"
            )

    def render(self, fb, frame_idx, t):

        for i in range(50):
            draw_noise_line(fb)

        fb *= 0.94







def draw_text(fb_width, fb_height, x, y, font_size, text):
    img = np.zeros((height, width, 3), dtype=np.uint8)

    font.putText(img,
        text=text,
        org=(x, y),
        fontHeight=font_size,
        color=(0, 0, 255),
        thickness=-1,
        line_type=cv2.LINE_AA,
        bottomLeftOrigin=False,
    )

    # Convert to float32
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

# Simulate a beat
sim_beat = False
if len(sys.argv) == 2 and sys.argv[1] == '--sim_beat':
    sim_beat = True

beatclient = BeatClient()

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

anim = MerryHS()

beat_idx = 0

for frame_idx in itertools.count(start=0):

    start_t = time.time()

    if beatclient.beat_received() or (sim_beat and frame_idx % 15 == 0):
        print("|" * 40)
        anim.beat(fb, beat_idx, start_t)
        beat_idx += 1
    else:
        print()
    
    anim.render(fb, frame_idx, start_t)

    # Show the current frame
    cv2.imshow('image', fb) 

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
    end_t = time.time()
    frame_t = end_t - start_t
    fps = 1 / frame_t
    #print("fps: {:.1f}".format(fps))

    # Limit the update rate to 30fps
    t_30fps = 1 / 30
    if frame_t < t_30fps:
        #print(t_30fps - frame_t)
        time.sleep(t_30fps - frame_t)

cv2.destroyAllWindows()
