from image import *

class entity():
    def __init__(self, x:int = None, y:int = None, name:str = "unknown", size:int = 128, xMomentum:int = 0, yMomentum:int = 0, speed:int = 10, jumpForce:int = 5, gravitation:int = 2, isPlayer:bool = False, image = BALL):
        self.x = x
        self.y = y
        self.name = name
        self.size = size
        self.xMomentum = xMomentum
        self.yMomentum = yMomentum
        self.speed = speed
        self.jumpForce = jumpForce
        self.gravitation = gravitation
        self.isPlayer = isPlayer
        self.image = image
            
    def getLocation(self) -> tuple:
        return (self.x, self.y)
    
    def getCenter(self) -> tuple: # returns the location of center pixel of the model
        return self.x + self.size/2, self.y - self.size/2
    
    def setLocation(self, x:int, y:int):
        self.x = x
        self.y = y

    

    def jump(self, direction:int):
        self.yMomentum += self.jumpForce * direction

    def addMomentum(self, direction:int):
        self.xMomentum += direction * self.speed 
    
    def move(self):
        self.yMomentum -= self.gravitation
        self.setLocation(self.x + self.xMomentum, self.y - (self.yMomentum))
        self.slowdown()


    def slowdown(self): # slowsdown movement speed to make the game feel dynamic
        self.xMomentum = self.xMomentum * 0.8
        self.yMomentum = self.yMomentum * 0.8
        if abs(self.xMomentum) < 0.01:
            self.xMomentum = 0
        if abs(self.yMomentum) < 0.01:
            self.yMomentum = 0

        

    