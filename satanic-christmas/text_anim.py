#!/usr/bin/env python3

import cv2
import numpy as np   

# Load a custom font
font = cv2.freetype.createFreeType2()
font.loadFontData(fontFileName='ferrum.otf', id=0)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)

# Make window fullscreen
cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 1080p resolution, 16:9 aspect ration, like the projector
width = 1920
height = 1080

# Frame buffer
# In floating point format so we can fade out easily
fb = np.zeros((height, width, 3), dtype=np.float32)






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
