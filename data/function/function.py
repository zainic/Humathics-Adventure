import numpy as np
import cv2
import os, sys

from .object import *

def create_main_menu_frame(background ,layers = []):
    """
    Create frame from some condition

    Args:
        background (class, optional): background. Defaults to Background().
        layers (list, optional): layers that overlay the background. Defaults to [].
    """
    
    frame = np.copy(background.background)
    
    return frame
    
def get_exit_status(key):
    """
    function that return exit status from key pressed

    Args:
        key (int): key that got from cv2.waitKey()

    Returns:
        bool: exit status
    """
    
    if key == 27:
        return True
    
    return False