import numpy as np
import cv2
import os, sys

from pygame import mixer
from pynput import keyboard

from data.function.object import *
from data.function.function import *
from data.function.main_menu import *

def main():
    mixer.init()
    mixer.music.load(os.path.join("data","music","main_menu.mp3"))
    mixer.music.play(-1)
    
    listener = keyboard.Listener(on_press=on_pressed, on_release=on_released)
    listener.start()
    
    status = 'main_menu'
    
    while True:
        if status == 'main_menu':
            status = main_menu()
        elif status == 'exit':
            break
    
    listener.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()