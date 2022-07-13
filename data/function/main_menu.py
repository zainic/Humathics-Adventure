import numpy as np
import cv2
import os, sys

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
    
    listener = keyboard.Listener(on_press=on_pressed, on_release=on_released)
    listener.start()
    
    while True:
        frame = create_main_menu_frame(background, layers = [play_button, exit_button])
        
        cv2.imshow("Humathics Adventure", frame)
        
        key = cv2.waitKey(10) & 0xff
        
        background.move_background(LEFT, 2)
        
        print(pressed_keys)
        
        if get_exit_status(key):
            break
    
    listener.stop()
    