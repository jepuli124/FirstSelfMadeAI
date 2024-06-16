import random
from node import *

class selfAI():
    def __init__(self):
        self.input = []
        self.layers = [] 
        self.bridges = []   
        self.output = []
        self.networkLayerSize = 0

    def makeNewRandomNetwork(self, layerSize, layerAmount):
        for _ in range(layerAmount):
            layer = []
            bridge = []
            for y in range(layerSize):
                layer.append(node(random.random()))
                bridgeLine = []
                for x in range(layerSize): # bridge to each other node in the next tier
                    bridgeLine.append(random.random())
                bridge.append(bridgeLine.copy())
            self.layers.append(layer.copy())
            self.bridges.append(bridge)


        cube = [] # making last bridge as 3d tensor
        for z in range(layerSize):
            side = []
            for y in range(layerSize): 
                line = []
                for z in range(layerSize): 
                    line.append(random.random())
                side.append(line.copy()) 
            cube.append(side.copy())
        self.bridges[-1] = (cube.copy())
            
        self.networkLayerSize = layerSize
            

    def produceMap(self, mapSize):
        if mapSize[0] > self.networkLayerSize or mapSize[1] > self.networkLayerSize:
            print("Too small network\nNetwork size:", str(self.networkLayerSize), "\nAsked map size:", mapSize, "\nMap's size should be at maxium the networks size")
            return None
        
        map = [] #making base for the map. Randomizing start makes output to be unique 
        for y in range(mapSize[1]):
            line = []
            for x in range(mapSize[0]):
                line.append(random.random())
            map.append(line.copy())
        
        print("random map:")
        for line in map:
            print(line)

        self.output = map.copy()
        self.runNetwork(map, mapSize)

        print("AI output map")
        for line in self.output:
            print(line)

        return self.output
    
    def runNetwork(self, map, mapSize):
        self.input = map   
        self.calculateInputToTier(self.input, self.layers[0])
        for layer in range(len(self.layers)-1):
            self.calculateNextTier(self.layers[layer], self.layers[layer + 1], self.bridges[layer])
        self.calculateLastTierToOutput(self.layers[-1], self.output, self.bridges[-1], mapSize)


    def calculateNextTier(self, previousTier, nextTier, layerBridge):
        for xLocation, x in enumerate(nextTier):
            x.output = 0
            sum = 0
            counter = 0
            for yLocation, y in enumerate(previousTier):
                sum += (layerBridge[yLocation][xLocation] * y.output) 
                counter += 1
            sum /= counter
            if sum >= x.bias:
                x.output = 1

    def calculateInputToTier(self, previousTier, nextTier):
        for x in nextTier:
            x.output = 0
            sum = 0
            counter = 0
            for line in previousTier:
                for y in line:
                    sum += y
                    counter += 1
            sum /= counter
            if sum >= x.bias:
                x.output = 1

    def calculateLastTierToOutput(self, previousTier, output, layerBridge, mapSize):
        for yOutput in range(mapSize[1]):
            for xOutput in range(mapSize[0]):
                sum = 0
                counter = 0
                for yLocation, y in enumerate(previousTier):
                    sum += (layerBridge[yLocation][yOutput][xOutput] * y.output) 
                    counter += 1
                sum /= counter
                output[yOutput][xOutput] = sum


ai = selfAI()
ai.makeNewRandomNetwork(6, 4)
# for x in ai.bridgei1:
#     print(x[1])

ai.produceMap((4, 4))