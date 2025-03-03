import cv2
import pyautogui
import time
from handtracking_module import HandTrace
from screeninfo import get_monitors
import numpy as np

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FPS, 60)

hand = HandTrace(max_num_hands=1)

def frame2screen(fX, fY):
    for monitor in get_monitors():
        s_width = monitor.width
        s_height = monitor.height
    
    f_height, f_width = frame.shape[0], frame.shape[1]

    sX = np.interp(fX, [0, f_width], [0, s_width]).astype(int)
    sY = np.interp(fY, [0, f_height], [0, s_height]).astype(int)

    return (sX, sY)

pyautogui.FAILSAFE = False

def move(frame, input_id):
    (x, y) = hand.id2axes(frame, input_id)
    (x, y) = frame2screen(x, y)
    pyautogui.moveTo(x, y, duration=0.0001)


while True:
    success, frame = camera.read()
    frame = cv2.flip(frame, 1)

    move(frame, 8)