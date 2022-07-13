import numpy as np
import cv2
import os, sys

from .object import *
from .function import *

def main_menu(pressed_keys):
    """
    Main menu phase
    """
    background = Background(os.path.join("data", "texture", "main_menu", "background.png"))
    while True:
        frame = create_main_menu_frame(background)
        
        cv2.imshow("Humathics Adventure", frame)
        
        key = cv2.waitKey(10) & 0xff
        
        background.move_background(LEFT, 2)
        
        if get_exit_status(key):
            break
    