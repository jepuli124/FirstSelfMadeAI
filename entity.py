from image import *

class entity():
    def __init__(self, x = None, y = None, xMomentum = 0, yMomentum = 0, speed = 10, jumpForce = 5, gravitation = 2, isPlayer = False, image = BALL):
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
        self.yMomentum -= self.gravitation
        self.setLocation(self.x + self.xMomentum, self.y - (self.yMomentum))
        self.slowdown()


    def slowdown(self):
        self.xMomentum = self.xMomentum * 0.8
        self.yMomentum = self.yMomentum * 0.9

        if abs(self.xMomentum) < 0.01:
            self.xMomentum = 0
        if abs(self.yMomentum) < 0.01:
            self.yMomentum = 0

        

    