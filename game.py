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
        hight = 0
        returnableMap = []
        for line in map:
            hight += 1
            if len(line) > length:
                length = len(line)

        for line in range(length):
            xAxis = ["air"] * hight
            returnableMap.append(xAxis.copy())

        for xnumber, x in enumerate(map):
            for ynumber, y in enumerate(x):
                match y:
                    case "b":
                        returnableMap[ynumber][xnumber] = "block"
                    case "t":
                        returnableMap[ynumber][xnumber] = "triangle"
                    case "s":
                        returnableMap[ynumber][xnumber] = "start"
                    case "e":
                        returnableMap[ynumber][xnumber] = "end"
                    case _:
                        pass

    return m.map(returnableMap)


def newFrame(map, EntitiesList):
    pygame.draw.rect(window, (0,0,0), [0, 0, windowSize[0], windowSize[1]])
    for xtimes, x in enumerate(map.objects):
        for ytimes, y in enumerate(x):
            match y:
                case "block":
                    window.blit(BLOCK, (128*(xtimes), 128*(ytimes)))
                case "triangle":
                    window.blit(SPIKE, (128*(xtimes), 128*(ytimes)))
                case "start":
                    window.blit(BALL, (128*(xtimes), 128*(ytimes)))
                case "end":
                    window.blit(BALL, (128*(xtimes), 128*(ytimes)))
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
    run = True
    clock = pygame.time.Clock()
    FPS = 30
    map = mapDecoder()
    EntitiesList = []
    EntitiesList.append(e.entity(x = None, y = None, xMomentum = 0, yMomentum = 0, speed = 10, jumpForce = 5, gravitation = 1, isPlayer = True))
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_ESCAPE]:
            run = False
            break
        playerActions(pressedKeys, EntitiesList[0])
        
        map, EntitiesList = upkeep(map, EntitiesList)

        newFrame(map, EntitiesList)
        clock.tick(FPS)

    return


gameLoop()

pygame.quit()

