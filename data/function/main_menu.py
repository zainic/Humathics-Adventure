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
    Created main menu pages

    Returns:
        str: status after exiting main menu page
    """
    background = Background(os.path.join("data", "texture", "main_menu", "background.png"))
    play_button = Button(os.path.join("data", "texture", "main_menu", "play_button_selected.png"), os.path.join("data", "texture", "main_menu", "play_button.png"))
    exit_button = Button(os.path.join("data", "texture", "main_menu", "exit_button_selected.png"), os.path.join("data", "texture", "main_menu", "exit_button.png"))
    
    play_button.toggle_button()
    
    levels_button = {}
    for i in range(15):
        levels_button[((i//5) + 1, (i % 5) + 1)] = Button(os.path.join("data", "texture", "main_menu", "level_"+ str(i+1) +"_selected.png"), os.path.join("data", "texture", "main_menu", "level_"+ str(i+1) +".png"))
    
    back_button = Button(os.path.join("data", "texture", "main_menu", "back_to_main_menu_selected.png"), os.path.join("data", "texture", "main_menu", "back_to_main_menu.png"))
    
    switch_button = mixer.Sound(os.path.join("data","sound","switch_button.wav"))
    select_button = mixer.Sound(os.path.join("data","sound","select_button.wav"))
    delay_enter = 5
    
    st = time.time()
    
    while True:
        
        frame = create_main_menu_frame(background, layers = [play_button, exit_button])
        
        ed = time.time()
        show_fps(frame, st, ed)
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
        
        if get_enter_status(pressed_keys) and delay_enter <= 0:
            mixer.Sound.play(select_button)
            if play_button.select == True:
                stat = 'level_selection'
            elif exit_button.select == True:
                stat = 'exit'
            break
        else:
            delay_enter -= 1
    
    current_pos = np.array([1,1])
    levels_button[(current_pos[0], current_pos[1])].toggle_button()
    delay_move = 5
    delay_enter = 5
    time.sleep(0.5)
    
    while stat == 'level_selection':
        
        frame = create_level_selection_frame(background, layers = list(levels_button.values()) + [back_button])
        
        ed = time.time()
        show_fps(frame, st, ed)
        st = time.time()
        
        cv2.imshow("Humathics Adventure", frame)
        
        key = cv2.waitKey(1) & 0xff
        
        background.move_background(LEFT, 2)
        
        direction = get_direction_from_keys(pressed_keys)
        
        if delay_move <= 0 and 1 <= current_pos[0] + direction[0] <= 3 and 1 <= current_pos[1] + direction[1] <= 5 and not (direction == NO_MOVE).all():
            if back_button.select == True:
                back_button.toggle_button()
            else:
                before_pos = np.copy(current_pos)
                levels_button[(before_pos[0],before_pos[1])].toggle_button()
            current_pos += direction
            levels_button[(current_pos[0],current_pos[1])].toggle_button()
            delay_move = 5
            mixer.Sound.play(switch_button)
        elif delay_move <= 0 and current_pos[0] + direction[0] == 4 and current_pos[1] + direction[1] == current_pos[1] and not (direction == NO_MOVE).all():
            before_pos = np.copy(current_pos)
            levels_button[(before_pos[0],before_pos[1])].toggle_button()
            current_pos += direction
            back_button.toggle_button()
            delay_move = 5
            mixer.Sound.play(switch_button)
        else:
            delay_move -= 1
        
        if get_enter_status(pressed_keys) and delay_enter <= 0:
            mixer.Sound.play(select_button)
            if back_button.select:
                stat = 'main_menu'
            else:
                level = (current_pos[0] - 1) * 5 + current_pos[1]
                print(level)
                stat = 'level' + str(level)
            break
        else:
            delay_enter -= 1
        
    ed = time.time()
    return stat
    