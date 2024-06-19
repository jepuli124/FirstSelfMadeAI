import random


def run(size: tuple):
    map = []
    for y in range(size[1]):
        map.append([" "] * size[0])

    map = generateMap(map) 
    writeFile(map)


def generateMap(map: list) -> list:
    for yLocation, y in enumerate(map):
        for xLocation, x in enumerate(map):
            match random.randint(0, 3):
                case 1:
                    map[yLocation][xLocation] = "b" #block
                case 2:
                    map[yLocation][xLocation] = "t" #spike

    map[random.randint(0, len(map)-1)][random.randint(0, len(map[0])-1)] = "e" #end point
    map[random.randint(0, len(map)-1)][random.randint(0, len(map[0])-1)] = "s" #start point
    return map
            
def writeFile(map: list):
    fileNameCounter = 0
    run = True
    while run:
        try:
            file = open("map/random"+ str(fileNameCounter) +".txt", "xt")
            run = False
        except:
            fileNameCounter += 1
    for line in map:
        for object in line:
            file.write(object) 
        file.write("\n")   
    file.close()