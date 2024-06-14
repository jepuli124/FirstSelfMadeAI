from image import *

class entity():
    def __init__(self, x = None, y = None, name = "unknown", size = 128, xMomentum = 0, yMomentum = 0, speed = 10, jumpForce = 5, gravitation = 2, isPlayer = False, image = BALL):
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
            
    def getLocation(self):
        return (self.x, self.y)
    
    def getCenter(self): # returns the location of center pixel of the model
        return self.x + self.size/2, self.y - self.size/2
    
    def setLocation(self, x, y):
        self.x = x
        self.y = y

    

    def jump(self, direction):
        self.yMomentum += self.jumpForce * direction

    def addMomentum(self, direction):
        self.xMomentum += direction * self.speed 
    
    def move(self):
        #self.yMomentum -= self.gravitation
        self.setLocation(self.x + self.xMomentum, self.y - (self.yMomentum))
        self.slowdown()


    def slowdown(self): # slowsdown movement speed to make the game feel dynamic
        self.xMomentum = self.xMomentum * 0.8
        self.yMomentum = self.yMomentum * 0.9

        if abs(self.xMomentum) < 0.01:
            self.xMomentum = 0
        if abs(self.yMomentum) < 0.01:
            self.yMomentum = 0

        

    