import numpy as np
import cv2
import os, sys

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
        self.texture = cv2.imread(texture_path)

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
        self.texture = cv2.imread(texture_path)

class LevelLayer(Layer):
    def __init__(self, texture_path, solid = False):
        """
        Initial to load level layer

        Args:
            texture_path (str): path of the layer image texture for level with black background
            solid (bool, optional): . Defaults to False.
        """
        super().__init__(texture_path)
        self.solid = solid

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
        self.texture = cv2.imread(texture_path)