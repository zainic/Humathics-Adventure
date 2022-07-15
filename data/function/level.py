import numpy as np
import cv2
import os, sys
import time

from PIL import Image
from pygame import mixer
from pynput import keyboard

from .object import *
from .function import *

def level_stage_1():
    """
    Created level stage

    Args:
        number_level (int): number of level
    
    Returns:
        str: status after exiting level stage phase
    """
    
    level_stage_background_list = ["background_type_1.png"]
    
    background = Background(os.path.join("data", "texture", "levels", level_stage_background_list[np.random.randint(0,1)]))
    layer_1 = LevelLayer(os.path.join("data", "texture", "levels", "layer_level_1_1.png"), solid=True, hurt=False)
    layer_2 = LevelLayer(os.path.join("data", "texture", "levels", "layer_level_1_2.png"), solid=False, hurt=False)
    layer_3 = LevelLayer(os.path.join("data", "texture", "levels", "layer_level_1_3.png"), solid=True, hurt=True)
    
    layers = [layer_1, layer_2, layer_3]
    layer_PIL = Image.new("RGBA", (background.background.shape[1], background.background.shape[0]))
    for layer in layers:
        texture = cv2.cvtColor(np.copy(layer.texture), cv2.COLOR_BGRA2RGBA)
        texture_PIL = Image.fromarray(texture)
        layer_PIL.paste(texture_PIL, (0,0), texture_PIL)
    
    switch_button = mixer.Sound(os.path.join("data","sound","switch_button.wav"))
    select_button = mixer.Sound(os.path.join("data","sound","select_button.wav"))
    delay_enter = 5
    
    st = time.time()
    
    while True:
        
        frame = create_level_frame(background, layers = [layer_PIL])
        
        ed = time.time()
        show_fps(frame, st, ed)
        st = time.time()
        
        cv2.imshow("Humathics Adventure", frame)
        
        key = cv2.waitKey(1) & 0xff
        
        background.move_background(LEFT, 2)
        
        if get_exit_status(pressed_keys) and delay_enter <= 0:
            mixer.Sound.play(select_button)
            ed = time.time()
            return 'exit'
        else:
            delay_enter -= 1