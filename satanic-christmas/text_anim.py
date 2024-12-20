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
import argparse

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

    def beat(self, fb, beat_idx, t):
        pass

    def render(self, fb, frame_idx, t):
        raise NotImplementedError

class MerryGlitch(Anim):
    def __init__(self, fb_shape):
        pass

        merry = draw_text(
            fb.shape[0],
            fb.shape[1],
            x=220,
            y=300,
            font_size=260,
            text="Merry Christmas"
        )

        hs = draw_text(
            fb.shape[0],
            fb.shape[1],
            x=460,
            y=300,
            font_size=260,
            text="Hail Satan"
        )

        self.merry_frames = [np.random.uniform(0, 1, size=fb_shape) * glitch(merry, 5) for i in range(16)]
        self.hs_frames = [np.random.uniform(0, 1, size=fb_shape) * glitch(hs, 4) for i in range(16)]

        self.glitch_count = 0

    def render(self, fb, frame_idx, t):
        if random.uniform(0, 1) < 0.025: 
            fb[:] = random.choice(self.hs_frames)[:]
            self.glitch_count = random.uniform(0, 3)
            return

        if self.glitch_count > 0:
            self.glitch_count -= 1
            return

        fb[:] = random.choice(self.merry_frames)[:]

class MerryHS(Anim):
    def __init__(self, fb_shape):
        pass

    def beat(self, fb, beat_idx, t):
        #fb[:] = 0

        if beat_idx % 16 == 0:
            fb += draw_text(
                fb.shape[0],
                fb.shape[1],
                x=220,
                y=300,
                font_size=260,
                text="Merry Christmas"
            )
        elif beat_idx % 16 == 8:
            fb += draw_text(
                fb.shape[0],
                fb.shape[1],
                x=460,
                y=300,
                font_size=260,
                text="Hail Satan"
            )

    def render(self, fb, frame_idx, t):
        for i in range(60):
            draw_noise_line(fb)
        fb *= 0.995

class Korhal(Anim):
    def __init__(self, fb_shape):
        # Pre-render KORHAL text
        self.korhal = draw_text(
            fb_shape[0],
            fb_shape[1],
            x=220,
            y=180,
            font_size=500,
            text="KORHAL"
        )

        self.on = draw_text(
            fb_shape[0],
            fb_shape[1],
            x=445,
            y=700,
            font_size=200,
            text="ON THE"
        )

        self.the_decks = draw_text(
            fb_shape[0],
            fb_shape[1],
            x=1050,
            y=700,
            font_size=200,
            text="DECKS"
        )

        # Pre-render some noise
        self.noise = [np.random.uniform(0, 1, size=fb_shape) for i in range(0, 8)]

        # Bounds of the letters
        self.letter_exts = [
            (230, 480),
            (480, 740),
            (740, 960),
            (960, 1240),
            (1240, 1500),
            (1500, 1720),
        ]

    def beat(self, fb, beat_idx, t):
        beat_idx = beat_idx % 8

        if beat_idx < 6:
            l_min, l_max = self.letter_exts[beat_idx % len(self.letter_exts)]
            fb[:, l_min:l_max] += self.korhal[:, l_min:l_max]
        elif beat_idx == 6:
            fb += self.on
        else:
            fb += self.the_decks

    def render(self, fb, frame_idx, t):
        for i in range(60):
            draw_noise_line(fb)
        fb *= 0.97

class Rescue(Anim):
    def __init__(self, fb_shape):
        # Pre-render RESCUE text
        self.rescue = draw_text(
            fb_shape[0],
            fb_shape[1],
            x=220,
            y=180,
            font_size=500,
            text="RESCUE"
        )

        self.on_the_decks = draw_text(
            fb_shape[0],
            fb_shape[1],
            x=445,
            y=700,
            font_size=200,
            text="ON THE DECKS"
        )

        self.frames = [self.render_frame(fb_shape, i) for i in range(0, 30)]
    
        self.f_idx = 0

    def render_frame(self, fb_shape, frame_idx):
        fb = self.rescue.copy()
        fb += self.on_the_decks
        fb *= np.random.uniform(0, 1, size=fb.shape) 

        ratio = 1 - (frame_idx / 30)
        scale = math.floor(ratio * 8)

        print(scale)

        fb[:] = glitch(fb, scale) * (ratio * ratio)

        return fb

    def beat(self, fb, beat_idx, t):
        self.f_idx = 0

    def render(self, fb, frame_idx, t):
        f_idx = self.f_idx
        self.f_idx += 1

        if f_idx < len(self.frames):
            frame = self.frames[f_idx]
        else:
            frame = random.choice(self.frames[-4:])
    
        fb[:] = frame

def glitch(img, scale=2):
    out = np.empty_like(img)

    for row in range(0, img.shape[0]):
        if random.uniform(0, 1) < 0.1:
            out[row] = 0
        else:
            shift = int(np.random.normal(scale=scale))
            out[row] = np.roll(img[row], shift, axis=0)

    # Vertical shift
    shift = int(np.random.normal(scale=scale))
    out = np.roll(out, shift, axis=0)

    return out

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


parser = argparse.ArgumentParser()
parser.add_argument('--sim_beat', action='store_true')
parser.add_argument('--fullscreen', action='store_true')
opts = parser.parse_args()

beatclient = BeatClient()

# Load a custom font
font = cv2.freetype.createFreeType2()
font.loadFontData(fontFileName='ferrum.otf', id=0)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)

# Make window fullscreen
if opts.fullscreen:
    cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 1080p resolution, 16:9 aspect ration, like the projector
width = 1920
height = 1080

# Frame buffer
# In floating point format so we can fade out easily
fb = np.zeros((height, width, 3), dtype=np.float32)

normal_anims = [
    MerryGlitch(fb.shape),
    MerryHS(fb.shape),
]
rescue_anims = normal_anims + [Rescue(fb.shape)]
korhal_anims = normal_anims + [Korhal(fb.shape)]

anim = normal_anims[0]

mode = 'normal'

beat_idx = 0

for frame_idx in itertools.count(start=0):

    start_t = time.time()

    if beatclient.beat_received() or (opts.sim_beat and frame_idx % 15 == 0):
        print("|" * 40)

        # Switch animation
        if beat_idx > 0 and beat_idx % 32 == 0:
            print('SWITCH ****')
            if mode == 'normal':
                anim = random.choice(normal_anims)
            elif mode == 'rescue':
                anim = random.choice(rescue_anims)
            elif mode == 'korhal':
                anim = random.choice(korhal_anims)

        anim.beat(fb, beat_idx, start_t)
        beat_idx += 1
    else:
        print()
        anim.render(fb, frame_idx, start_t)

    # Show the current frame
    cv2.imshow('image', fb) 
  
    end_t = time.time()
    frame_t = end_t - start_t
    fps = 1 / frame_t
    #print("fps: {:.1f}".format(fps))

    # Limit the update rate to 30fps
    t_30fps = 1 / 30
    if frame_t < t_30fps:
        #print(t_30fps - frame_t)
        time.sleep(t_30fps - frame_t)

    # Quit when 'q' is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('n'):
        mode = 'normal'
    elif key == ord('r'):
        mode = 'rescue'
        cv2.rectangle(fb, (20, 910), (25, 915), (0, 0, 255), 1)
    elif key == ord('k'):
        mode = 'korhal'
        cv2.rectangle(fb, (1800, 910), (1805, 915), (0, 0, 255), 1)

cv2.destroyAllWindows()
