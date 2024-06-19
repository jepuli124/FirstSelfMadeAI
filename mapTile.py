from image import *

class mapTile():
    def __init__(self, name:str, x:int = None, y:int = None, size:int = 128, image = BLOCK):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.image = image