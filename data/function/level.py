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
    
    Returns:
        str: status after exiting level stage phase
    """
    
    level_stage_background_list = ["background_type_1.png"]
    
    background = Background(os.path.join("data", "texture", "levels", level_stage_background_list[np.random.randint(0,1)]))
    coordinates = Coordinates(tick = 70*WINDOW_HEIGHT//360, origin = np.array([WINDOW_HEIGHT//2 - 20*WINDOW_HEIGHT//360, WINDOW_WIDTH//2]))
    layer_1 = LevelLayer(os.path.join("data", "texture", "levels", "layer_level_1_1.png"), solid=True, hurt=False)
    layer_2 = LevelLayer(os.path.join("data", "texture", "levels", "layer_level_1_2.png"), solid=False, hurt=False)
    layer_3 = LevelLayer(os.path.join("data", "texture", "levels", "layer_level_1_3.png"), solid=True, hurt=True)
    layer_4 = Layer(os.path.join("data", "texture", "levels", "layer_level_default_1.png"))
    
    level_star = {}
    level_star["1"] = Button(os.path.join("data", "texture", "levels", "star_collected.png"), os.path.join("data", "texture", "levels", "star_uncollected.png"))
    level_star["2"] = Button(os.path.join("data", "texture", "levels", "star_collected.png"), os.path.join("data", "texture", "levels", "star_uncollected.png"))
    level_star["3"] = Button(os.path.join("data", "texture", "levels", "star_collected.png"), os.path.join("data", "texture", "levels", "star_uncollected.png"))
    
    star = {}
    star["1"] = Object(os.path.join("data", "texture", "levels", "star.png"), coordinates.coord_to_pixel(np.array([2,0])))
    star["2"] = Object(os.path.join("data", "texture", "levels", "star.png"), coordinates.coord_to_pixel(np.array([1,-1])))
    star["3"] = Object(os.path.join("data", "texture", "levels", "star.png"), coordinates.coord_to_pixel(np.array([1,1])))
    
    shapebox = (11*WINDOW_HEIGHT//360, 22*WINDOW_WIDTH//640, 32*WINDOW_HEIGHT//360, 195*WINDOW_WIDTH//640)
    equation = TextBox("Equation", fixed=True, background_color=(10,77,148), shapebox=shapebox, font_style=cv2.FONT_HERSHEY_COMPLEX_SMALL)
    
    node = {}
    node["origin"] = Object(os.path.join("data", "texture", "levels", "origin.png"), coordinates.coord_to_pixel(np.array([0,0])))
    for i in np.arange(-10,11,1):
        if coordinates.coord_to_pixel(np.array([0,i]))[0] != -1 and i != 0:
            node[(0,i)] = Object(os.path.join("data", "texture", "levels", "node.png"), coordinates.coord_to_pixel(np.array([0,i])))
        if coordinates.coord_to_pixel(np.array([i,0]))[1] != -1 and i != 0:
            node[(i,0)] = Object(os.path.join("data", "texture", "levels", "node.png"), coordinates.coord_to_pixel(np.array([i,0])))
    
    layers = [layer_1, layer_2, layer_3, layer_4]
    layer_PIL = Image.new("RGBA", (background.background.shape[1], background.background.shape[0]))
    for layer in layers:
        layer_PIL.paste(layer.texture_PIL, (0,0), layer.texture_PIL)
    
    switch_button = mixer.Sound(os.path.join("data","sound","switch_button.wav"))
    select_button = mixer.Sound(os.path.join("data","sound","select_button.wav"))
    delay_enter = 5
    delay_type = 3
    
    st = time.time()
    
    while True:
        
        frame = create_level_frame(background, layers = [layer_PIL], objects = list(level_star.values()) + list(star.values()) + list([equation]) + list(node.values()))
        
        ed = time.time()
        show_fps(frame, st, ed)
        st = time.time()
        
        cv2.imshow("Humathics Adventure", cv2.resize(frame, None, fx=DEFAULT_WINDOW_WIDTH/WINDOW_WIDTH, fy=DEFAULT_WINDOW_HEIGHT/WINDOW_HEIGHT, interpolation=cv2.INTER_NEAREST))
        
        key = cv2.waitKey(1) & 0xff
        
        background.move_background(LEFT, 2)
        char = get_char(pressed_keys)
        
        if char != None and delay_type <= 0:
            equation.add_letter(char)
            delay_type = 3
        elif get_backspace(pressed_keys) and delay_type <= 0:
            equation.backspace()
            delay_type = 3
        else:
            delay_type -= 1
        equation.update_box()
        
        if get_exit_status(pressed_keys) and delay_enter <= 0:
            mixer.Sound.play(select_button)
            ed = time.time()
            return 'exit'
        else:
            delay_enter -= 1