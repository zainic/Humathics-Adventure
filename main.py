import numpy as np
import cv2
import os, sys

from pygame import mixer
from pynput import keyboard

from data.function.object import *
from data.function.function import *
from data.function.main_menu import *
from data.function.level import *

def main():
    mixer.init()
    
    main_menu_music_list = ["main_menu_1.mp3", "main_menu_2.mp3"]
    
    mixer.music.load(os.path.join("data","music",main_menu_music_list[np.random.randint(0,len(main_menu_music_list))]))
    mixer.music.play(-1)
    
    listener = keyboard.Listener(on_press=on_pressed, on_release=on_released)
    listener.start()
    
    status = 'main_menu'
    
    while True:
        if status == 'main_menu':
            status = main_menu()
        elif status[:5] == "level":
            if int(status[-1]) == 1:
                status = level_stage_1()
        elif status == 'exit':
            break
    
    listener.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()