from image import *

class entity():
    def __init__(self, x = None, y = None, xMomentum = 0, yMomentum = 0, speed = 10, jumpForce = 5, gravitation = 1, isPlayer = False, image = BALL):
        self.x = x
        self.y = y
        self.xMomentum = xMomentum
        self.yMomentum = yMomentum
        self.speed = speed
        self.jumpForce = jumpForce
        self.gravitation = gravitation
        self.isPlayer = isPlayer
        self.image = image
            
    def getLocation(self):
        return (self.x, self.y)
    
    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def jump(self):
        self.yMomentum += self.jumpForce

    def addMomentum(self, direction):
        self.xMomentum += direction * self.speed 
    
    def move(self):
        self.setLocation(self.x + self.xMomentum, self.y + self.yMomentum - self.gravitation)

    