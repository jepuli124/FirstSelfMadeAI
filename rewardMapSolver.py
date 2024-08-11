import mapSolverAI
import math
def rewardPath(AI: mapSolverAI) -> float:
    reward = 100 - AI.hitWallTotal
    previousMove = -1
    cumulativeSameMovePenalty = 0
    for move in AI.path:
        if move == previousMove:
            reward -= 2 - cumulativeSameMovePenalty
            cumulativeSameMovePenalty += 1
        else:
            cumulativeSameMovePenalty = 0
        previousMove = move
        if move == 0:
            reward -= 1
        if move == -1:
            reward += 2
        if move == -3:
            reward -= 3

    reward += math.dist(AI.currentLocation, AI.endLocation) * (-1)  
    return reward