import pygame
import math
import entity as e
import mapTile as mT
import map as m
from image import * 

# the global variables
windowSize = (1280, 720)
window = None

def start():
    global window
    pygame.init()
    
    windowSize = (1280, 720)
    window = pygame.display.set_mode(windowSize)

    pygame.display.set_caption("game")


    font = pygame.font.Font('freesansbold.ttf', 150)
    starttext = font.render("Loading", True, (255, 255, 255))
    window.blit(starttext, ((windowSize[0]/2)-300, (windowSize[1]/2)-75))
    pygame.display.flip()


def mapDecoder(mapName:str) -> m.map:
    try:
        with open("map/"+mapName+".txt") as mapfile:
            map = mapfile.readlines()
            length = 0
            hight = 0
            returnableMap = []
            for line in map:
                hight += 1
                if len(line) > length:
                    length = len(line)

            for line in range(length):
                xAxis = [None] * hight
                returnableMap.append(xAxis.copy())

            for ynumber, y in enumerate(map):
                for xnumber, x in enumerate(y):
                    match x:
                        case "b":
                            returnableMap[xnumber][ynumber] = mT.mapTile("block", x = 128*(xnumber), y = 128*(ynumber), image= BLOCK)
                        case "t":
                            returnableMap[xnumber][ynumber] = mT.mapTile("triangle", x = 128*(xnumber), y = 128*(ynumber), image= SPIKE)
                        case "s":
                            returnableMap[xnumber][ynumber] = mT.mapTile("start", x = 128*(xnumber), y = 128*(ynumber), image= BALL)
                        case "e":
                            returnableMap[xnumber][ynumber] = mT.mapTile("end", x = 128*(xnumber), y = 128*(ynumber), image= BALL)
                        case _:
                            pass

        return m.map(returnableMap)
    except:
        print("map not found")
        return False


def newFrame(map, entitiesList: list):
    pygame.draw.rect(window, (0,0,20), [0, 0, windowSize[0], windowSize[1]])
    for x in map.objects:
       for tile in x:
           if tile == None:
               continue
           window.blit(tile.image, relativeLocationOfToPlayer(entitiesList[0], tile))
            

    for entity in entitiesList:
        if entity.x != None:
            if entity == entitiesList[0]:
                window.blit(entity.image, ((windowSize[0]/2) - entity.size/2, (windowSize[1]/2) + entity.size/2))
            else:
                window.blit(entity.image, (entity.x, entity.y))

    
    pygame.display.flip()

# def relativeLocationOfTileToPlayer(player, tileX, tileY):
#     x = 128*(tileX)-player.x+windowSize[0]/2
#     y = 128*(tileY)-player.y+windowSize[1]/2
#     return x, y

def relativeLocationOfToPlayer(player, entity: e.entity) -> tuple:
    x = (entity.x)-player.getCenter()[0]+windowSize[0]/2
    y = (entity.y)-player.getCenter()[1]+windowSize[1]/2
    return x, y

def playerActions(pressedKeys: list, player: e.entity):
    if pressedKeys[pygame.K_w] or pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_SPACE]:
        player.jump(1)
    if pressedKeys[pygame.K_a] or pressedKeys[pygame.K_LEFT]:
        player.addMomentum(-1)
    if pressedKeys[pygame.K_s] or pressedKeys[pygame.K_DOWN]:
        player.jump(-1)
    if pressedKeys[pygame.K_d] or pressedKeys[pygame.K_RIGHT]:
        player.addMomentum(1)


def upkeep(map: list, entitiesList: list) -> tuple: # collection of misc. actions to keep game going 
    if entitiesList[0].x == None:
        startX, startY =  tileLocation("start", map) 
        if startX != None:
            entitiesList[0].setLocation(startX, startY)

    moveEntities(entitiesList)
    collisionHandler(map, entitiesList)
    return map, entitiesList

def moveEntities(entitiesList: list):
    for entity in entitiesList:
        if entity.x != None:
            entity.move()

def tileLocation(name: str, map: list) -> tuple:
    for x in map.objects:
        for y in x:
            if y == None:
               continue
            if y.name == name:
                return y.x, y.y
                
    return None

def collisionHandler(map: list, entitiesList: list):
    for entity1 in range(len(entitiesList)):
        for entity2 in range(entity1 + 1, len(entitiesList)):
            collisionChecker(entitiesList[entity1], entitiesList[entity2])
        for line in map.objects:
            for tile in line:
                if tile == None or tile.image == BALL:
                    continue
                loop, side = collisionChecker(entitiesList[entity1], tile)
                
                while loop: 
                    #if loop: print(entitiesList[entity1].getCenter())
                    match side:
                        case "xNegative":
                            entitiesList[entity1].x = math.floor(entitiesList[entity1].x) - 1
                            entitiesList[entity1].xMomentum = 0

                        case "xPositive":
                            entitiesList[entity1].x = math.floor(entitiesList[entity1].x) + 1
                            entitiesList[entity1].xMomentum = 0

                        case "yNegative":
                            entitiesList[entity1].y = math.floor(entitiesList[entity1].y) - 1
                            entitiesList[entity1].yMomentum = 0

                        case "yPositive":
                            entitiesList[entity1].y = math.floor(entitiesList[entity1].y) + 1
                            entitiesList[entity1].yMomentum = 0

                    loop, _ = collisionChecker(entitiesList[entity1], tile)




def collisionChecker(object1: e.entity, object2: e.entity) -> tuple:
    object1CornerPoints = [(object1.x, object1.y), (object1.x+object1.size, object1.y), (object1.x, object1.y+object1.size), (object1.x+object1.size, object1.y+object1.size)] 
    for pointNumber, point in enumerate(object1CornerPoints):
        if (point[0] <= object2.x + object2.size and point[0] >= object2.x) and (point[1] <= object2.y + object2.size and point[1] >= object2.y):
            xNegative = abs(point[0] - object2.x)
            xPositive = abs(point[0] - (object2.x + object2.size))
            yNegative = abs(point[1] - object2.y)
            yPositive = abs(point[1] - (object2.y + object2.size)) 
            match pointNumber:
                case 0:
                    if yPositive > xPositive:
                        return True, "xPositive"
                    else:
                        return True, "yPositive"
                case 1:
                    if yPositive > xNegative:
                        return True, "xNegative"
                    else:
                        return True, "yPositive"
                case 2:
                    if yNegative > xPositive:
                        return True, "xPositive"
                    else:
                        return True, "yNegative"
                case 3:
                    if yNegative > xNegative:
                        return True, "xNegative"
                    else:
                        return True, "yNegative"
    return False, ""
    

def endGame(pressedKeys: list) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    if pressedKeys[pygame.K_ESCAPE]:
        return True
        
            

def gameLoop(fileName: str):
    run = True
    clock = pygame.time.Clock()
    FPS = 30
    map = mapDecoder(fileName)
    if map == False:
        return
    entitiesList = []
    entitiesList.append(e.entity(x = None, y = None, speed = 10, jumpForce = 10, isPlayer = True))
    while run:
        
        pressedKeys = pygame.key.get_pressed()

        if endGame(pressedKeys):
            run = False
            break

        playerActions(pressedKeys, entitiesList[0])
        
        map, entitiesList = upkeep(map, entitiesList)

        newFrame(map, entitiesList)
        
        clock.tick(FPS)

    return

def end():
    pygame.quit()


#gameLoop()

#pygame.quit()

