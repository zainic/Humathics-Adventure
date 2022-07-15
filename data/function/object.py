import numpy as np
import cv2
import os, sys

from PIL import Image

DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 720

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
        self.full_background = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
        self.background = self.full_background[:DEFAULT_WINDOW_HEIGHT, :DEFAULT_WINDOW_WIDTH]
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
        if (self.y % self.full_background.shape[0]) + DEFAULT_WINDOW_HEIGHT >= self.full_background.shape[0]:
            self.background = np.vstack([self.full_background[self.y :, :], self.full_background[:DEFAULT_WINDOW_HEIGHT - (self.full_background.shape[0] - self.y), :]])
        else:
            self.background = self.full_background[self.y : self.y + DEFAULT_WINDOW_HEIGHT, :]
            
        self.x = (self.x - X * step) % self.full_background.shape[1]
        if (self.x % self.full_background.shape[1]) + DEFAULT_WINDOW_WIDTH >= self.full_background.shape[1]:
            self.background = np.hstack([self.full_background[:, self.x:], self.full_background[:, :DEFAULT_WINDOW_WIDTH - (self.full_background.shape[1] - self.x)]])
        else:
            self.background = self.full_background[:, self.x : self.x + DEFAULT_WINDOW_WIDTH]

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
        self.texture = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
        
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
    def __init__(self, texture_path):
        """
        Initial to load the object

        Args:
            layer_path (str): path of the layer image with black background
        """
        self.texture = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)
        
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
        self.unselected = cv2.imread(texture_unselected_path, cv2.IMREAD_UNCHANGED)
        self.selected = cv2.imread(texture_selected_path, cv2.IMREAD_UNCHANGED)
        
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
        