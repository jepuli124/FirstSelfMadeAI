import pygame
import entity as e
import mapTile as mT
import map as m
from image import * 

pygame.init()

windowSize = (1280, 720)
window = pygame.display.set_mode(windowSize)

pygame.display.set_caption("game")

# A1 = pygame.image.load("pict/Bg.png") example code
# window.blit(A1, (0, 0))
font = pygame.font.Font('freesansbold.ttf', 150)
starttext = font.render("Loading", True, (255, 255, 255))
window.blit(starttext, ((windowSize[0]/2)-300, (windowSize[1]/2)-75))
pygame.display.flip()


# Loading images
#






def mapDecoder():
    with open("map/test.txt") as mapfile:
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


def newFrame(map, entitiesList):
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

def relativeLocationOfToPlayer(player, entity):
    x = (entity.x)-player.getCenter()[0]+windowSize[0]/2
    y = (entity.y)-player.getCenter()[1]+windowSize[1]/2
    return x, y

def playerActions(pressedKeys, player):
    if pressedKeys[pygame.K_w] or pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_SPACE]:
        player.jump(1)
    if pressedKeys[pygame.K_a] or pressedKeys[pygame.K_LEFT]:
        player.addMomentum(-1)
    if pressedKeys[pygame.K_s] or pressedKeys[pygame.K_DOWN]:
        player.jump(-1)
    if pressedKeys[pygame.K_d] or pressedKeys[pygame.K_RIGHT]:
        player.addMomentum(1)


def upkeep(map, entitiesList): # collection of misc. actions to keep game going 
    if entitiesList[0].x == None:
        startX, startY =  tileLocation("start", map) 
        if startX != None:
            entitiesList[0].setLocation(startX, startY)

    moveEntities(entitiesList)
    collisionHandler(map, entitiesList)
    return map, entitiesList

def moveEntities(entitiesList):
    for entity in entitiesList:
        if entity.x != None:
            entity.move()

def tileLocation(name, map):
    for x in map.objects:
        for y in x:
            if y == None:
               continue
            if y.name == name:
                return y.x, y.y
                
    return None

def collisionHandler(map, entitiesList):
    for entity1 in range(len(entitiesList)):
        for entity2 in range(entity1 + 1, len(entitiesList)):
            collisionChecker(entitiesList[entity1], entitiesList[entity2])
        for line in map.objects:
            for tile in line:
                if tile == None or tile.image == BALL:
                    continue
                loop, side, amount = collisionChecker(entitiesList[entity1], tile)
                
                while loop: 
                    #if loop: print(entitiesList[entity1].getCenter())
                    match side:
                        case "x":
                            entitiesList[entity1].x += amount - tile.size + 1
                            entitiesList[entity1].xMomentum = 0
                            print("to the x")
                        case "y":
                            entitiesList[entity1].y += amount - tile.size + 1
                            entitiesList[entity1].yMomentum = 0
                            print("to the y")
                    loop,side, amount = collisionChecker(entitiesList[entity1], tile)




def collisionChecker(object1, object2):
    xDistance = object1.x - object2.x
    yDistance = object1.y - object2.y
    if abs(xDistance) <= object1.size and abs(yDistance) <= object1.size:
        if abs(xDistance) > abs(yDistance):
                return True, "x", xDistance
        return True, "y", yDistance
    return False, "", 0

def endGame(pressedKeys):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    if pressedKeys[pygame.K_ESCAPE]:
        return True
        
            

def gameLoop():
    run = True
    clock = pygame.time.Clock()
    FPS = 30
    map = mapDecoder()
    entitiesList = []
    entitiesList.append(e.entity(x = None, y = None, speed = 5, jumpForce = 10, isPlayer = True))
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


gameLoop()

pygame.quit()

