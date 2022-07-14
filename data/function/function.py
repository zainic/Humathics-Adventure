import numpy as np
import cv2
import os, sys

from pynput import keyboard

from .object import *

global pressed_keys

pressed_keys = set()

def on_pressed(key):
    pressed_keys.add(key)

def on_released(key):
    pressed_keys.remove(key)

def create_main_menu_frame(background ,layers = []):
    """
    Create frame from some condition

    Args:
        background (class, optional): background. Defaults to Background().
        layers (list, optional): layers that overlay the background. Defaults to [].
    """
    
    frame = np.copy(background.background)
    button_counter = 0
    
    # Show layers
    for layer in layers:
        if layer.__name__ == "Button":
            button_counter += 1
            if layer.select == False:
                texture_unselected = np.copy(layer.unselected)
                position = (4 * frame.shape[0] // 5 - texture_unselected.shape[0] // 2 - 50, button_counter * frame.shape[1] // 3 - texture_unselected.shape[1] // 2)
                part_button = np.copy(frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]])
                part_button_overlay = cv2.addWeighted(part_button, 1, texture_unselected, 1, 2)
                frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]] = part_button_overlay
            else:
                texture_selected = np.copy(layer.selected)
                position = (4 * frame.shape[0] // 5 - texture_selected.shape[0] // 2 - 50, button_counter * frame.shape[1] // 3 - texture_selected.shape[1] // 2)
                part_button = np.copy(frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]])
                part_button_overlay = cv2.addWeighted(part_button, 1, texture_selected, 1, 2)
                frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]] = part_button_overlay
                
            
    
    return frame

def get_enter_status(pressed_keys):
    """
    function that return enter status from key pressed

    Args:
        pressed_keys (set): key that got pressed

    Returns:
        bool: exit status
    """
    if keyboard.Key.enter in pressed_keys:
        return True
    
    return False

def get_exit_status(pressed_keys):
    """
    function that return exit status from key pressed

    Args:
        pressed_keys (set): key that got pressed

    Returns:
        bool: exit status
    """
    if keyboard.Key.esc in pressed_keys:
        return True
    
    return False