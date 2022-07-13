import numpy as np
import cv2
import os, sys
import time

from pynput import keyboard

from .object import *
from .function import *

def main_menu():
    """
    Main menu phase
    """
    background = Background(os.path.join("data", "texture", "main_menu", "background.png"))
    play_button = Button(os.path.join("data", "texture", "main_menu", "play_button_selected.png"), os.path.join("data", "texture", "main_menu", "play_button.png"))
    exit_button = Button(os.path.join("data", "texture", "main_menu", "exit_button_selected.png"), os.path.join("data", "texture", "main_menu", "exit_button.png"))
    
    play_button.toggle_button()
    
    listener = keyboard.Listener(on_press=on_pressed, on_release=on_released)
    listener.start()
    st = time.time()
    
    delay_change_button = 5
    
    while True:
        
        frame = create_main_menu_frame(background, layers = [play_button, exit_button])
        
        ed = time.time()
        if ed - st <= 1/60:
            time.sleep(1/60 - (ed - st))
            fps = 60
        else:
            fps = round(1/(ed - st))
        cv2.putText(frame, "fps : " + str(fps), (10, DEFAULT_WINDOW_HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        st = time.time()
        
        cv2.imshow("Humathics Adventure", frame)
        
        key = cv2.waitKey(1) & 0xff
        
        background.move_background(LEFT, 2)
        
        if (keyboard.Key.right in pressed_keys or keyboard.Key.left in pressed_keys) and delay_change_button <= 0:
            play_button.toggle_button()
            exit_button.toggle_button()
            delay_change_button = 5
        else:
            delay_change_button -= 1
        
        if get_exit_status(pressed_keys):
            break
    
    ed = time.time()
    listener.stop()
    