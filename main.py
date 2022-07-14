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
    
    while True:
        status = main_menu()
        if status == 'level_selection':
            pass
        elif status == 'exit':
            break
        
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()