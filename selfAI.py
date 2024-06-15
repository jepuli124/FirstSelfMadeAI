import random
from node import *

class selfAI():
    def __init__(self):
        self.input = []
        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.bridge12 = []   # bridge between tiers 
        self.bridge23 = []
        self.output = []

    def makeNewRandomNetwork(self, size):
        for y in range(size):
            self.tier1.append(node(random.random()))
            self.tier2.append(node(random.random()))
            self.tier3.append(node(random.random()))
            line12 = []
            line23 = []
            for x in range(size): # bridge to each other node in the next tier
                line12.append(random.random())
                line23.append(random.random())
            self.bridge12.append(line12.copy())
            self.bridge23.append(line23.copy())
            

    def produceMap(self, mapSize):
        map = []
        for y in range(mapSize[1]):
            line = []
            for x in range(mapSize[0]):
                line.append(random.random())
            map.append(line.copy())

        self.runNetwork(map)
        return self.output
    
    def runNetwork(self, map):
        self.input = map   
        self.calculateTier(self.input, self.tier1)
        self.calculateTier(self.tier1, self.tier2, tierBridge = self.bridge12)
        self.calculateTier(self.tier2, self.tier3, tierBridge = self.bridge23)
        self.calculateTier(self.tier3, self.output)


    def calculateTier(self, previousTier, nextTier, tierBridge = None):
        for xLocation, x in enumerate(nextTier):
            x.output = 0
            sum = 0
            counter = 0
            for yLocation, y in enumerate(previousTier):
                if tierBridge != None:
                    sum += (tierBridge[yLocation][xLocation] * y) 
                else: sum += y
                counter += 1
            sum /= counter
            if sum >= x.bias:
                x.output = 1

    

ai = selfAI()
ai.makeNewRandomNetwork(6)
# for x in ai.bridgei1:
#     print(x[1])

print(ai.produceMap((4, 4)))