import numpy as np
import cv2
import os, sys
import time

from pygame import mixer
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
    
    switch_button = mixer.Sound(os.path.join("data","sound","switch_button.wav"))
    select_button = mixer.Sound(os.path.join("data","sound","select_button.wav"))
    
    listener = keyboard.Listener(on_press=on_pressed, on_release=on_released)
    listener.start()
    st = time.time()
    
    while True:
        
        frame = create_main_menu_frame(background, layers = [play_button, exit_button])
        
        ed = time.time()
        if ed - st <= 1/48:
            time.sleep(1/48 - (ed - st))
            fps = 48
        else:
            fps = round(1/(ed - st))
        cv2.putText(frame, "fps : " + str(fps), (10, DEFAULT_WINDOW_HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        st = time.time()
        
        cv2.imshow("Humathics Adventure", frame)
        
        key = cv2.waitKey(1) & 0xff
        
        background.move_background(LEFT, 2)
        
        if play_button.select == False and keyboard.Key.left in pressed_keys:
            play_button.set_button(True)
            exit_button.set_button(False)
            mixer.Sound.play(switch_button)
        elif exit_button.select == False and keyboard.Key.right in pressed_keys:
            exit_button.set_button(True)
            play_button.set_button(False)
            mixer.Sound.play(switch_button)
        
        if get_enter_status(pressed_keys):
            mixer.Sound.play(select_button)
            break
    
    time.sleep(1)
    ed = time.time()
    listener.stop()
    