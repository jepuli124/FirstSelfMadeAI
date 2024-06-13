import pygame

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


def mapDecoder(map):
    returnableMap = [["air"] * map.size[y]] * map.size[x]

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
    return returnableMap

def newFrame():
    
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
    pass

def moveEntities(entitiesList):
    for entity in entitiesList:
        entity.move()


def gameLoop():
    clock = pygame.time.Clock()
    FPS = 30
    map = None
    EntitiesList = []
    while True:
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_ESCAPE]:
            break
        playerActions(pressedKeys)
        map, EntitiesList = upkeep(map, EntitiesList)
        newFrame()
        clock.tick(FPS)

    return


gameLoop()

pygame.quit()

