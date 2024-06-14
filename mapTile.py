from image import *

class mapTile():
    def __init__(self, name, x = None, y = None, size = 128, image = BLOCK):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.image = image