import pygame
import entity as e
import map as m

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

BALL = pygame.image.load("Textures/ball.png")
BLOCK = pygame.image.load("Textures/block.png")
SPIKE = pygame.image.load("Textures/spike.png")




def mapDecoder():
    with open("map/test.txt") as mapfile:
        map = mapfile.readlines()
        length = 0
        for line in map:
            if len(line) > length:
                length = len(line)
        returnableMap = [["air"] * length] * len(map)

        for xnumber, x in enumerate(map):
            for ynumber, y in enumerate(x):
                match y:
                    case "b":
                        returnableMap[xnumber][ynumber] = "block"
                    case "t":
                        returnableMap[xnumber][ynumber] = "triangle"
                    case "s":
                        returnableMap[xnumber][ynumber] = "start"
                    case "e":
                        returnableMap[xnumber][ynumber] = "end"
                    case _:
                        pass
    for line in returnableMap:  
        print(line)
    return m.map(returnableMap)


def newFrame(map, EntitiesList):

    for xtimes, x in enumerate(map.objects):
        print("")
        for ytimes, y in enumerate(x):
            print(y, end="")
            match y:
                case "block":
                    window.blit(BLOCK, (128*(xtimes-1), 128*(ytimes-1)))
                case "triangle":
                    window.blit(SPIKE, (128*(xtimes-1), 128*(ytimes-1)))
                case "start":
                    window.blit(BALL, (128*(xtimes-1), 128*(ytimes-1)))
                case "end":
                    window.blit(BALL, (128*(xtimes-1), 128*(ytimes-1)))
                case _:
                    pass
            
    
    for entity in EntitiesList:
        if entity.x != None:
            window.blit(BALL, (entity.x, entity.y))
    
    pygame.display.flip()

def playerActions(pressedKeys, player):
    if pressedKeys[pygame.K_w] or pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_SPACE]:
        player.jump()
    if pressedKeys[pygame.K_a] or pressedKeys[pygame.K_LEFT]:
        player.addMomentum(-1)
    if pressedKeys[pygame.K_s] or pressedKeys[pygame.K_DOWN]:
        pass
    if pressedKeys[pygame.K_d] or pressedKeys[pygame.K_RIGHT]:
        player.addMomentum(1)


def upkeep(map, EntitiesList):
    return map, EntitiesList

def moveEntities(entitiesList):
    for entity in entitiesList:
        if entity.x != None:
            entity.move()


def gameLoop():
    clock = pygame.time.Clock()
    FPS = 30
    map = mapDecoder()
    EntitiesList = []
    EntitiesList.append(e.entity(x = None, y = None, xMomentum = 0, yMomentum = 0, speed = 10, jumpForce = 5, gravitation = 1, isPlayer = True))
    while True:
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_ESCAPE]:
            break
        playerActions(pressedKeys, EntitiesList[0])
        
        map, EntitiesList = upkeep(map, EntitiesList)

        newFrame(map, EntitiesList)
        clock.tick(FPS)
        break

    return


gameLoop()

pygame.quit()

