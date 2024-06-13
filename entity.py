class entity():
    def __init__(self):
        self.x = None
        self.y = None
        self.xMomentum = 0
        self.yMomentum = 0
        self.speed = 10
        self.jumpForce = 5
        self.gravitation = 1
            
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

    