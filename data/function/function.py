import numpy as np
import cv2
import os, sys
import time

from PIL import Image
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
    Create frame from some condition in main menu frame

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
                position = (4 * frame.shape[0] // 5 - texture_unselected.shape[0] // 2, button_counter * frame.shape[1] // 3 - texture_unselected.shape[1] // 2)
                part_button = np.copy(frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]])
                part_button = cv2.addWeighted(part_button, 1, texture_unselected, -255, 0)
                frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]] = cv2.addWeighted(part_button, 1, texture_unselected, 1, 0)
            else:
                texture_selected = np.copy(layer.selected)
                position = (4 * frame.shape[0] // 5 - texture_selected.shape[0] // 2, button_counter * frame.shape[1] // 3 - texture_selected.shape[1] // 2)
                part_button = np.copy(frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]])
                part_button = cv2.addWeighted(part_button, 1, texture_selected, -255, 0)
                frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]] = cv2.addWeighted(part_button, 1, texture_selected, 1, 0)
                
    return frame

def create_level_selection_frame(background ,layers = []):
    """
    Create frame from some condition in level selection page

    Args:
        background (class, optional): background. Defaults to Background().
        layers (list, optional): layers that overlay the background. Defaults to [].
    """
    
    frame = np.copy(background.background)
    button_counter = 0
    
    # Show layers
    for layer in layers:
        if layer.__name__ == "Button":
            if button_counter < 15:
                if layer.select == False:
                    texture_unselected = np.copy(layer.unselected)
                    position = (((button_counter//5) + 2) * frame.shape[0] // 6 - texture_unselected.shape[0] // 2 - 50, ((button_counter % 5) + 2) * frame.shape[1] // 8 - texture_unselected.shape[1] // 2)
                    part_button = np.copy(frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]])
                    part_button = cv2.addWeighted(part_button, 1, texture_unselected, -255, 0)
                    frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]] = cv2.addWeighted(part_button, 1, texture_unselected, 1, 0)
                else:
                    texture_selected = np.copy(layer.selected)
                    position = (((button_counter//5) + 2) * frame.shape[0] // 6 - texture_selected.shape[0] // 2 - 50, ((button_counter % 5) + 2) * frame.shape[1] // 8 - texture_selected.shape[1] // 2)
                    part_button = np.copy(frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]])
                    part_button = cv2.addWeighted(part_button, 1, texture_selected, -255, 0)
                    frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]] = cv2.addWeighted(part_button, 1, texture_selected, 1, 0)
            else:
                if layer.select == False:
                    texture_unselected = np.copy(layer.unselected)
                    position = (6 * frame.shape[0] // 7 - texture_unselected.shape[0] // 2, frame.shape[1] // 4 - texture_unselected.shape[1] // 2)
                    part_button = np.copy(frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]])
                    part_button = cv2.addWeighted(part_button, 1, texture_unselected, -255, 0)
                    frame[position[0] : position[0] + texture_unselected.shape[0], position[1] : position[1] + texture_unselected.shape[1]] = cv2.addWeighted(part_button, 1, texture_unselected, 1, 0)
                else:
                    texture_selected = np.copy(layer.selected)
                    position = (6 * frame.shape[0] // 7 - texture_selected.shape[0] // 2, frame.shape[1] // 4 - texture_selected.shape[1] // 2)
                    part_button = np.copy(frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]])
                    part_button = cv2.addWeighted(part_button, 1, texture_selected, -255, 0)
                    frame[position[0] : position[0] + texture_selected.shape[0], position[1] : position[1] + texture_selected.shape[1]] = cv2.addWeighted(part_button, 1, texture_selected, 1, 0)
            button_counter += 1
                    
    return frame

def create_level_frame(background ,layers = [], objects = []):
    """
    Create frame from some condition in level selection page

    Args:
        background (class, optional): background. Defaults to Background().
        layers (list, optional): layers that overlay the background. Defaults to [].
    """
    
    frame_PIL = background.background_PIL
    button_counter = 0
    object_counter = 0
    
    # Show layers
    for layer in layers:
        frame_PIL = Image.alpha_composite(frame_PIL, layer)
    
    for object in objects:
        if object.__name__ == "Button":
            if object.select:
                frame_PIL.paste(object.selected_PIL, (3*WINDOW_WIDTH//4 + object.unselected.shape[1] * button_counter, 5), object.selected_PIL)
            else:
                frame_PIL.paste(object.unselected_PIL, (3*WINDOW_WIDTH//4 + object.unselected.shape[1] * button_counter, 5), object.unselected_PIL)
            button_counter += 1
        elif object.__name__ == "Object":
            frame_PIL.paste(object.texture_PIL, (object.coord[0] - object.texture.shape[1]//2, object.coord[1] - object.texture.shape[0]//2), object.texture_PIL)
            object_counter += 1
        elif object.__name__ == "TextBox":
            TextBox_PIL = Image.fromarray(cv2.cvtColor(object.box, cv2.COLOR_BGR2RGBA))
            frame_PIL.paste(TextBox_PIL, (object.shapebox[1], object.shapebox[0]), TextBox_PIL)
    
    frame = cv2.cvtColor(np.array(frame_PIL), cv2.COLOR_RGBA2BGRA)
    
    return frame

def show_fps(frame, st, ed):
    """
    Show the frame rate (debugging mode)

    Args:
        frame (array): frame that will be showed
        st (float): start time process
        et (float): end time process
    """
    if ed - st <= 1/30:
        time.sleep(1/30 - (ed - st))
        fps = 30
    else:
        fps = round(1/(ed - st))
    cv2.putText(frame, "fps : " + str(fps), (10*WINDOW_WIDTH//640, WINDOW_HEIGHT - 10*WINDOW_HEIGHT//360), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1, cv2.LINE_AA)

def get_direction_from_keys(keys):
    """
    function that return direction for ship from key pressed

    Args:
        keys (set): keys that got from Listener

    Returns:
        array: direction 
    """
    
    direction = np.copy(NO_MOVE)
    
    if keyboard.Key.up in keys:
        direction += UP
    if keyboard.Key.down in keys:
        direction += DOWN
    if keyboard.Key.left in keys:
        direction += LEFT
    if keyboard.Key.right in keys:
        direction += RIGHT
        
    return direction

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

def get_char(pressed_keys):
    """
    funtion with char as return value

    Args:
        pressed_keys (set): key that got pressed

    Returns:
        str: character
    """
    for char in list(pressed_keys):
        try:
            if type(char.char) == type(""):
                return char.char
        except:
            pass
    
    return None

def get_backspace(pressed_keys):
    """
    function that return backspace pressed status from key pressed

    Args:
        pressed_keys (set): key that got pressed

    Returns:
        bool: backspace pressed status
    """
    if keyboard.Key.backspace in pressed_keys:
        return True
    
    return False