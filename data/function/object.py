import numpy as np
import cv2
import os, sys

from PIL import Image

DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360

SCALE_WIDTH = WINDOW_WIDTH / DEFAULT_WINDOW_WIDTH
SCALE_HEIGHT = WINDOW_HEIGHT / DEFAULT_WINDOW_HEIGHT

UP = np.array([-1, 0])
DOWN = np.array([1, 0])
LEFT = np.array([0, -1])
RIGHT = np.array([0, 1])
NO_MOVE = np.array([0, 0])

class Background:
    """
    Create class of background
    """
    def __init__(self, texture_path):
        """
        Initial to load for background

        Args:
            texture_path (str): path of the background image texture
        """
        self.full_background = cv2.resize(cv2.imread(texture_path, cv2.IMREAD_UNCHANGED), None, fx=SCALE_WIDTH, fy=SCALE_HEIGHT, interpolation=cv2.INTER_AREA)
        self.background = self.full_background[:WINDOW_HEIGHT, :WINDOW_WIDTH]
        self.background_PIL = Image.fromarray(cv2.cvtColor(self.background, cv2.COLOR_BGRA2RGBA))
        self.x = 0
        self.y = 0
        
        self.__name__ = "Background"
        
    def move_background(self, direction, step):
        """
        Move the background, so added the dynamic background

        Args:
            direction (array): direction of the movement
            step (int): speed of movement in pixel
        """
        Y,X = direction
        
        self.y = (self.y - Y * step) % self.full_background.shape[0]
        if (self.y % self.full_background.shape[0]) + WINDOW_HEIGHT >= self.full_background.shape[0]:
            self.background = np.vstack([self.full_background[self.y :, :], self.full_background[:WINDOW_HEIGHT - (self.full_background.shape[0] - self.y), :]])
        else:
            self.background = self.full_background[self.y : self.y + WINDOW_HEIGHT, :]
            
        self.x = (self.x - X * step) % self.full_background.shape[1]
        if (self.x % self.full_background.shape[1]) + WINDOW_WIDTH >= self.full_background.shape[1]:
            self.background = np.hstack([self.full_background[:, self.x:], self.full_background[:, :WINDOW_WIDTH - (self.full_background.shape[1] - self.x)]])
        else:
            self.background = self.full_background[:, self.x : self.x + WINDOW_WIDTH]
            
        self.background_PIL = Image.fromarray(cv2.cvtColor(self.background, cv2.COLOR_BGRA2RGBA))

class Coordinates:
    """
    Create class of coordinates
    """
    def __init__(self, tick = 10, origin = np.array([WINDOW_HEIGHT//2, WINDOW_WIDTH//2])):
        """
        Create coordinate system with 2 axis (x,y)

        Args:
            tick (int, optional): tick pixel per one unit. Defaults to 10.
            origin (array, optional): center of coordinates (0,0) based on image pixel. Defaults to np.array([WINDOW_WIDTH//2, WINDOW_HEIGHT//2]).
        """
        y_axis = np.arange((WINDOW_HEIGHT-origin[0])/tick, (-origin[0])/tick, -1/tick)
        x_axis = np.arange((-origin[1])/tick, (WINDOW_WIDTH - origin[1])/tick, 1/tick)
        self.coords = np.array([[(i,j) for i in y_axis] for j in x_axis])
    
    def coord_to_pixel(self, coord):
        """
        Convert coordinate value into index/pixel value 

        Args:
            coord (array): Coordinate value [y,x]

        Returns:
            tuple: index of nearest value of the coord [i,j] if the coord value isn't in range, it returns [-1,-1]
        """
        diff = np.linalg.norm(self.coords - coord, axis=2)
        ind = np.unravel_index(np.argmin(diff, axis=None), diff.shape)
        if diff[ind] <= 1e-10:
            return np.array(ind)
        return np.array([-1,-1])
        
    def pixel_to_coord(self, pixel):
        """
        Convert index value into coordinate value corresponding to that index pixel

        Args:
            pixel (tuple): index of the pixel [i,j]

        Returns:
            array: Coordinate value [y,x]
        """
        return self.coords[pixel]

class Layer:
    """
    Create class of layer that will overlay the background
    """
    def __init__(self, texture_path):
        """
        Initial to load the layer

        Args:
            texture_path (str): path of the layer image texture with black background
            solid (bool, optional): . Defaults to False.
        """
        self.texture = cv2.resize(cv2.imread(texture_path, cv2.IMREAD_UNCHANGED), None, fx=SCALE_WIDTH, fy=SCALE_HEIGHT, interpolation=cv2.INTER_AREA)
        self.texture_PIL = Image.fromarray(cv2.cvtColor(self.texture, cv2.COLOR_BGRA2RGBA))
        
        self.__name__ = "Layer"

class LevelLayer(Layer):
    def __init__(self, texture_path, solid = False, hurt = False):
        """
        Initial to load level layer

        Args:
            texture_path (str): path of the layer image texture for level with black background
            solid (bool, optional): . Defaults to False.
        """
        super().__init__(texture_path)
        self.solid = solid
        self.hurt = hurt
        
        self.__name__ = "LevelLayer"

class Object:
    """
    Create class of object and 
    """
    def __init__(self, texture_path, coord = np.array([0,0])):
        """
        Initial to load the object

        Args:
            layer_path (str): path of the layer image with black background
        """
        self.texture = cv2.resize(cv2.imread(texture_path, cv2.IMREAD_UNCHANGED), None, fx=SCALE_WIDTH, fy=SCALE_HEIGHT, interpolation=cv2.INTER_AREA)
        self.texture_PIL = Image.fromarray(cv2.cvtColor(self.texture, cv2.COLOR_BGRA2RGBA))
        self.coord = coord
        
        self.__name__ = "Object"
        
class Button:
    """
    Create button class
    """
    def __init__(self, texture_selected_path, texture_unselected_path):
        """
        Initial load the button

        Args:
            texture_unselected_path (str): path of the unselected button texture with black background
            texture_selected_path (str): path of the selected button texture with black background
        """
        self.unselected = cv2.resize(cv2.imread(texture_unselected_path, cv2.IMREAD_UNCHANGED), None, fx=SCALE_WIDTH, fy=SCALE_HEIGHT, interpolation=cv2.INTER_AREA)
        self.selected = cv2.resize(cv2.imread(texture_selected_path, cv2.IMREAD_UNCHANGED), None, fx=SCALE_WIDTH, fy=SCALE_HEIGHT, interpolation=cv2.INTER_AREA)
        
        self.unselected_PIL = Image.fromarray(cv2.cvtColor(self.unselected, cv2.COLOR_BGRA2RGBA))
        self.selected_PIL = Image.fromarray(cv2.cvtColor(self.selected, cv2.COLOR_BGRA2RGBA))
        
        self.select = False
        
        self.__name__ = "Button"
    
        
    def toggle_button(self):
        """
        Turn on or off selected button
        """
        if self.select == True:
            self.select = False
        else:
            self.select = True
            
    def set_button(self, set):
        """
        Set the button status

        Args:
            set (boolean): Set the button status
        """
        self.select = set

class TextBox:
    """
    Create class of textbox
    """
    def __init__(self, initial_text = "", font_color = (255,255,255), background_color = (0,0,0), fixed = False, shapebox = (0,0,50,50),
                 font_style = cv2.FONT_HERSHEY_SIMPLEX, line = cv2.LINE_AA, font_scale = WINDOW_WIDTH/640):
        """
        Initial value of text box

        Args:
            initial_text (str, optional): Shown text. Defaults to "".
            font_color (tuple, optional): Font color. Defaults to (255,255,255) white in BGR.
            background_color (tuple, optional): Background color or behind text color. Defaults to (0,0,0) black in BGR.
            fixed (bool, optional): Fixed box position and stay. Defaults to False.
            shapebox (tuple, optional): Boundary of the text (up, left, bottom, right). Defaults to (0,0,50,50).
            font_style (int, optional): Font style. Defaults to cv2.FONT_HERSHEY_SIMPLEX.
            line (int, optional): Line style. Defaults to cv2.LINE_AA.
            font_scale (float, optional): Scale of font. Defaults to WINDOW_WIDTH/640.
        """
        self.text = initial_text
        self.color = font_color
        self.fill = background_color
        self.font = font_style
        self.fixed = fixed
        self.shapebox = shapebox
        self.line = line
        self.scale = font_scale
        
        self.box = np.zeros((self.shapebox[2]-self.shapebox[0], self.shapebox[3]-self.shapebox[1], 3), dtype=np.uint8) + np.array(list(self.fill), dtype=np.uint8)
        text_width, text_height = cv2.getTextSize(self.text, self.font, self.scale, self.line)[0]
        if self.fixed and text_width >= self.shapebox[3] - self.shapebox[1]:
            self.box = cv2.putText(self.box, self.text, ((self.shapebox[3] - self.shapebox[1])-text_width, (round(self.scale)*4 - 1 )*text_height//(round(self.scale)*4)), self.font, self.scale, self.color, 1, cv2.LINE_AA)
        else:
            self.box = cv2.putText(self.box, self.text, (0, (round(self.scale)*4 - 1 )*text_height//(round(self.scale)*4)), self.font, self.scale, self.color, 1, cv2.LINE_AA)
            
        self.__name__ = "TextBox"
        
    def add_letter(self, letter):
        """
        Update the text

        Args:
            letter (str): letter that'll be added into text box 
        """
        self.text += letter
        
    def backspace(self):
        """
        Remove one character from front
        """
        self.text = self.text[:-1]
        
    def update_box(self):
        """
        Update the text box
        """
        self.box = np.zeros((self.shapebox[2]-self.shapebox[0], self.shapebox[3]-self.shapebox[1], 3), dtype=np.uint8) + np.array(list(self.fill), dtype=np.uint8)
        text_width, text_height = cv2.getTextSize(self.text, self.font, self.scale, self.line)[0]
        if self.fixed and text_width >= self.shapebox[3] - self.shapebox[1]:
            self.box = cv2.putText(self.box, self.text, ((self.shapebox[3] - self.shapebox[1])-text_width, (round(self.scale)*4 - 1 )*text_height//(round(self.scale)*4)), self.font, self.scale, self.color, 1, cv2.LINE_AA)
        else:
            self.box = cv2.putText(self.box, self.text, (0, (round(self.scale)*4 - 1 )*text_height//(round(self.scale)*4)), self.font, self.scale, self.color, 1, cv2.LINE_AA)
  