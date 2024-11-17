#!/usr/bin/env python3

import cv2
import numpy as np   

# Load a custom font
font = cv2.freetype.createFreeType2()
font.loadFontData(fontFileName='ferrum.otf', id=0)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)

# Make window fullscreen
cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)






while True:

    # Use a 16:9 aspect ratio
    # What is the default 1080p resolution? 1920x1080
    img = np.zeros((720, 1280, 3), dtype=np.uint8)



    font.putText(img=img,
        text='Merry Christmas',
        org=(200, 200),
        fontHeight=140,
        color=(0, 0, 255),
        thickness=-1,
        line_type=cv2.LINE_AA,
        bottomLeftOrigin=False,
    )





    cv2.line(
        img,
        (0, 0),
        (700, 700),
        color=(0, 0, 0),
        lineType=cv2.LINE_AA,
        thickness=1
    )



    # Show the current frame
    cv2.imshow('image', img) 



    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  







cv2.destroyAllWindows()
