import cv2
import pyautogui
import time
from handtracking_module import HandTrace
from screeninfo import get_monitors
import numpy as np
import math

# --- SETUP ---
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FPS, 60)

hand = HandTrace(max_num_hands=1)

# OPTIMIZATION: Get screen size ONCE, not every frame
# Note: This takes the first monitor found. If you have dual screens, 
# you might need to select a specific index like monitors[1]
monitors = get_monitors()
s_width = monitors[0].width
s_height = monitors[0].height

pyautogui.FAILSAFE = False

def frame2screen(fX, fY, f_width, f_height):
    # Map coordinates from Camera space to Screen space
    sX = np.interp(fX, [0, f_width], [0, s_width])
    sY = np.interp(fY, [0, f_height], [0, s_height])
    
    # THE FIX: Clamp values to ensure they are within screen bounds.
    # This prevents the "struct.error" on Linux.
    sX = np.clip(sX, 0, s_width)
    sY = np.clip(sY, 0, s_height)

    return int(sX), int(sY)

def move(frame, input_id):
    # Get raw coordinates from hand tracker
    coords = hand.id2axes(frame, input_id)
    
    # SAFETY: Check if hand was actually detected
    # (Assuming id2axes returns None or empty if no hand found)
    if coords is None:
        return

    x, y = coords

    # SAFETY: Check if x or y are NaN (Not a Number) which causes crashes
    if math.isnan(x) or math.isnan(y):
        return

    f_height, f_width = frame.shape[:2]
    
    # Convert to screen coordinates
    screen_x, screen_y = frame2screen(x, y, f_width, f_height)
    
    # Move mouse
    pyautogui.moveTo(screen_x, screen_y, duration=0.0001)

# --- MAIN LOOP ---
while True:
    success, frame = camera.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)

    try:
        move(frame, 8)
    except Exception as e:
        # This catches any random errors without killing the camera feed
        print(f"Error in movement: {e}")

    # Optional: Display the frame to see what's happening
    cv2.imshow("Cursor Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
