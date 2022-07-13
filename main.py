import numpy as np
import cv2
import os, sys

from pynput import keyboard

from data.function.object import *
from data.function.function import *
from data.function.main_menu import *

global pressed_keys

pressed_keys = set()

def on_pressed(key):
    pressed_keys.add(key)

def on_released(key):
    pressed_keys.remove(key)

def main():
    listener = keyboard.Listener(on_press=on_pressed, on_release=on_released)
    listener.start()
    main_menu(pressed_keys)
    listener.stop()

if __name__ == "__main__":
    main()