import pathfinding
import sys

class Node:
    def __init__(self,parent, x,y, isMax,Value = None):
        self.X = x
        self.Y = y
        self.Parent = parent
        self.Childs = []
        self.Value = Value
        self.isMax = isMax
        self.Allpoints = 0


def minimax(grid,player,ghosts,foodList):
    playerPosition = ((player.rect.bottomright[1]-16)/32,(player.rect.bottomright[0]-16)/32)
    ghostsCoordinates = []
    for ghost in ghosts:
        ghostsCoordinates.append(((ghost.rect.bottomright[1]-16)/32,(ghost.rect.bottomright[0]-16)/32))
    
    possiblePlayerPoints = getPossiblePointsToGo(grid,playerPosition[0],playerPosition[1])

    nearestGhost = ghostsCoordinates[0]

    for item in ghostsCoordinates:
        if pathfinding.heuristic(((playerPosition[0]),(playerPosition[1])),(item[0],item[1]), "m") < pathfinding.heuristic(((playerPosition[0]),(playerPosition[1])),(nearestGhost[0],nearestGhost[1]), "m"):
          nearestGhost = item

    possibleGhostPoints = getPossiblePointsToGo(grid,nearestGhost[0],nearestGhost[1])

    nearestFood = getNearestFood((playerPosition[0],playerPosition[1]),foodList,grid)

    decision = Node(None,None,None,True)
    for item in possiblePlayerPoints:
        decision.Childs.append(Node(decision,item[0],item[1],False))

    for posiiblePlayerPosition in decision.Childs:
        for posiibleGhostPosition in possibleGhostPoints:
            distanceToGhost = pathfinding.heuristic(((posiiblePlayerPosition.X),(posiiblePlayerPosition.Y)),(posiibleGhostPosition[0],posiibleGhostPosition[1]), "es")
            distanceToFood = pathfinding.heuristic(((posiiblePlayerPosition.X),(posiiblePlayerPosition.Y)),(nearestFood[0],nearestFood[1]), "es")*1000
            if distanceToGhost <= 1:
                posiiblePlayerPosition.Childs.append(Node(posiiblePlayerPosition,posiibleGhostPosition[0],posiibleGhostPosition[1],False,-99999))
            elif distanceToFood == 0:
                posiiblePlayerPosition.Childs.append(Node(posiiblePlayerPosition,posiibleGhostPosition[0],posiibleGhostPosition[1],False,9999+distanceToGhost-distanceToFood))
            else:
                posiiblePlayerPosition.Childs.append(Node(posiiblePlayerPosition,posiibleGhostPosition[0],posiibleGhostPosition[1],False,distanceToGhost-distanceToFood))

    for posiiblePlayerPosition in decision.Childs:
        possibleGhostDecision = sys.maxsize
        for posiibleGhostPosition in posiiblePlayerPosition.Childs:
            if posiibleGhostPosition.Value < possibleGhostDecision:
              possibleGhostDecision = posiibleGhostPosition.Value
              posiiblePlayerPosition.Value = possibleGhostDecision

    playerDecision = -sys.maxsize
    decisionCoordinates = None
    for posiiblePlayerPosition in decision.Childs:
        if posiiblePlayerPosition.Value > playerDecision:
          playerDecision = posiiblePlayerPosition.Value
          decisionCoordinates = posiiblePlayerPosition

    return decisionCoordinates


def expectimax(grid,player,ghosts,foodList):
    playerPosition = ((player.rect.bottomright[1]-16)/32,(player.rect.bottomright[0]-16)/32)
    ghostsCoordinates = []
    for ghost in ghosts:
        ghostsCoordinates.append(((ghost.rect.bottomright[1]-16)/32,(ghost.rect.bottomright[0]-16)/32))
    
    possiblePlayerPoints = getPossiblePointsToGo(grid,playerPosition[0],playerPosition[1])

    nearestGhost = ghostsCoordinates[0]

    for item in ghostsCoordinates:
        if pathfinding.heuristic(((playerPosition[0]),(playerPosition[1])),(item[0],item[1]), "m") < pathfinding.heuristic(((playerPosition[0]),(playerPosition[1])),(nearestGhost[0],nearestGhost[1]), "m"):
          nearestGhost = item

    possibleGhostPoints = getPossiblePointsToGo(grid,nearestGhost[0],nearestGhost[1])

    nearestFood = getNearestFood((playerPosition[0],playerPosition[1]),foodList,grid)

    decision = Node(None,None,None,True)
    for item in possiblePlayerPoints:
        decision.Childs.append(Node(decision,item[0],item[1],False))

    for posiiblePlayerPosition in decision.Childs:
        for posiibleGhostPosition in possibleGhostPoints:
            distanceToGhost = pathfinding.heuristic(((posiiblePlayerPosition.X),(posiiblePlayerPosition.Y)),(posiibleGhostPosition[0],posiibleGhostPosition[1]), "es")
            distanceToFood = pathfinding.heuristic(((posiiblePlayerPosition.X),(posiiblePlayerPosition.Y)),(nearestFood[0],nearestFood[1]), "es")*100
            if distanceToGhost <= 1:
                posiiblePlayerPosition.Childs.append(Node(posiiblePlayerPosition,posiibleGhostPosition[0],posiibleGhostPosition[1],False,-99999))
            else:
                posiiblePlayerPosition.Childs.append(Node(posiiblePlayerPosition,posiibleGhostPosition[0],posiibleGhostPosition[1],False,distanceToGhost-distanceToFood))


    for posiiblePlayerPosition in decision.Childs:
        possibleGhostDecision = 0
        count = 0
        for posiibleGhostPosition in posiiblePlayerPosition.Childs:
            possibleGhostDecision += posiibleGhostPosition.Value
            count+=1
        posiiblePlayerPosition.Value = possibleGhostDecision/count

    playerDecision = -sys.maxsize
    decisionCoordinates = None
    for posiiblePlayerPosition in decision.Childs:
        if posiiblePlayerPosition.Value > playerDecision:
          playerDecision = posiiblePlayerPosition.Value
          decisionCoordinates = posiiblePlayerPosition



    return decisionCoordinates

def getNearestFood(playerPosition,foodList,field = None):
    playerPosition = (int(playerPosition[0]),int(playerPosition[1]))
    minDistance = sys.maxsize
    coordinates = None
    for item in foodList:
        distance = pathfinding.heuristic(((playerPosition[0]),(playerPosition[1])),((((item.rect.y-12)/32),(item.rect.x-12)/32)), "es")
        if distance <= minDistance:
          minDistance = distance
          coordinates = item
    nearest = ((((coordinates.rect.y-12)/32),(coordinates.rect.x-12)/32))
    return nearest


def getPossiblePointsToGo(field,x,y):
    x = int(x)
    y = int(y)
    high = len(field)
    wid = len(field[0])
    aroundPoints = []
    if x + 1 < high and field[x+1][y] > 0:
        aroundPoints.append((x+1,y))
    if x - 1 >= 0 and field[x-1][y] > 0:
      aroundPoints.append((x-1,y))
    if y + 1 < wid and field[x][y+1] > 0:
      aroundPoints.append((x,y+1))
    if y - 1 >= 0 and field[x][y-1] > 0:
      aroundPoints.append((x,y-1))

    return aroundPoints