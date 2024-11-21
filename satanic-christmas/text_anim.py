#!/usr/bin/env python3

import time
import math
import random
from threading import Thread
import aubio
import numpy as np
import sounddevice as sd
import cv2
import socket



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









text = draw_text(width, height)
fb += text
















while True:


    if beatclient.beat_received():
        print("|" * 40)
    else:
        print()
    






    for i in range(10):
        draw_noise_line(fb)

    fb *= 0.999
    # Show the current frame
    cv2.imshow('image', fb) 

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  







cv2.destroyAllWindows()