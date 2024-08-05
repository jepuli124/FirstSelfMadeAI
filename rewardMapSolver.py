import mapSolverAI
import math
def rewardPath(AI: mapSolverAI) -> float:
    reward = 100 - AI.hitWallTotal
    previousMove = -1
    for move in AI.path:
        if move == previousMove and move != 0:
            reward -= 2
        previousMove = move
        if move == -1:
            reward += 2
        if move == -3:
            reward -= 1
    reward += math.dist(AI.currentLocation, AI.endLocation) * (-1)  
    return reward