import enemies
from game import*
import sys

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREENWIDTH = 672
SCREENHEIGHT = 640

# #створення допоміжного поля для алгоритму BFS
# def newGrid():
#     addGrid = []
#     for i in range(len(enemies.grid)):
#         row = []
#         for j in range(len(enemies.grid[i])):
#             row.append(0)
#         addGrid.append(row)
#     return addGrid

# #метод реалізації "кроку" для пошуку в ширину
# def stepBfs(k, addGrid):
#     for i in range(len(addGrid)):
#         for j in range(len(addGrid[i])):
#             if addGrid[i][j] == k:
#                 if i>0 and addGrid[i-1][j] == 0 and enemies.grid[i-1][j] == 1:
#                     addGrid[i-1][j] = k + 1
#                 if j>0 and addGrid[i][j-1] == 0 and enemies.grid[i][j-1] == 1:
#                     addGrid[i][j-1] = k + 1
#                 if i<len(addGrid)-1 and addGrid[i+1][j] == 0 and enemies.grid[i+1][j] == 1:
#                     addGrid[i+1][j] = k + 1
#                 if j<len(addGrid[i])-1 and addGrid[i][j+1] == 0 and enemies.grid[i][j+1] == 1:
#                     addGrid[i][j+1] = k + 1

# #метод реалізації покрокового проходження поля для пошуку в ширину
# def findPathForBfs(addGrid, i, j):
#     k = addGrid[i][j]
#     path = [(i, j)]
#     while k > 1:
#         if i > 0 and addGrid[i - 1][j] == k-1:
#             i, j = i-1, j
#             path.append((i, j))
#             k-=1
#         elif j > 0 and addGrid[i][j - 1] == k-1:
#             i, j = i, j-1
#             path.append((i, j))
#             k-=1
#         elif i < len(addGrid) - 1 and addGrid[i + 1][j] == k-1:
#             i, j = i+1, j
#             path.append((i, j))
#             k-=1
#         elif j < len(addGrid[i]) - 1 and addGrid[i][j + 1] == k-1:
#             i, j = i, j+1
#             path.append((i, j))
#             k -= 1
#     return path

# #метод реалізації пошуку в ширину
# def bfs(startI, startJ, endI, endJ):
#     startI = int(startI)
#     startJ = int(startJ)
#     endI = int(endI)
#     endJ = int(endJ)
#     addGrid = newGrid()
#     addGrid[startI][startJ] = 1
#     k = 1
#     while addGrid[endI][endJ] == 0:
#         stepBfs(k, addGrid)
#         k += 1
#     path = findPathForBfs(addGrid, endI, endJ)
#     path.reverse()
#     return path

#створення списку для точок шляху
pathDfs = []
#метод реалізації пошуку шляху в глибину
def pathForDfs(startI, startJ, endI, endJ):
    startI = int(startI)
    startJ = int(startJ)
    endI = int(endI)
    endJ = int(endJ)
    gridForDfs = []
    for rows in enemies.grid:
        row = []
        for item in rows:
            row.append(item)
        gridForDfs.append(row)
    pathes = []
    dfs(startI, startJ, endI, endJ, pathes, gridForDfs)
    return pathes[0]

#метод реалізації роботи алгоритму пошуку в глибину
def dfs(startI, startJ, endI, endJ, pathes, gridForDfs):
    if startI < 0 or startJ < 0 or startI > len(gridForDfs)-1 or startJ > len(gridForDfs[0])-1:
        return
    if (startI, startJ) in pathDfs or gridForDfs[startI][startJ] < 1:
        return
    pathDfs.append((startI, startJ))
    gridForDfs[startI][startJ] = -1
    if(startI, startJ) != (endI, endJ):
        dfs(startI - 1, startJ, endI, endJ, pathes, gridForDfs)  # check top
        dfs(startI + 1, startJ, endI, endJ, pathes, gridForDfs)  # check bottom
        dfs(startI, startJ + 1, endI, endJ, pathes, gridForDfs)  # check right
        dfs(startI, startJ - 1, endI, endJ, pathes, gridForDfs)  # check left
    else:
        pathes.append(pathDfs.copy())
        pathDfs.pop()
        return 
    pathDfs.pop()
    return 

def ucs(mazeForUcs, startX, startY, endX, endY):
    maze = mazeForUcs
    startX = int(startX)*2
    startY = int(startY)*2
    endX = int(endX)*2
    endY = int(endY)*2

    # list of Nodes (with coordinates)
    listOfNodes = []
    # Nodes weights
    listOfWeights = []

    listOfNodes.append(Node(startX, startY, None))
    listOfWeights.append(0)

    # randomize weights for fields
    newGrid, visited = randomizeWeights(maze)

    startNode = None
    path = []
    while len(listOfNodes) > 0:
        minIndex = listOfWeights.index(min(listOfWeights))
        node = listOfNodes[minIndex]
        weightNode = listOfWeights[minIndex]
        newGrid[node.X][node.Y] = weightNode 
        listOfWeights[minIndex] = sys.maxsize

        startNode = Node(node.X, node.Y, startNode)
        visited[node.X][node.Y] = 1

        # if we find endpoint
        if node.X == endX and node.Y == endY:
            path = findPathUcs(node)
            return path

        tempArray = []
        tempWeightIndexesArray = []
        if node.X - 2 >= 0 and visited[node.X - 2][node.Y] != 1:
            tempArray.append(Node(node.X - 2, node.Y,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X - 1][node.Y])
        if node.Y - 2 >= 0 and visited[node.X][node.Y - 2] != 1:
            tempArray.append(Node(node.X, node.Y - 2,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X][node.Y - 1])
        if node.X + 2 < len(newGrid) and visited[node.X + 2][node.Y] != 1:
            tempArray.append(Node(node.X + 2, node.Y,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X + 1][node.Y])
        if node.Y + 2 < len(newGrid[0]) and visited[node.X][node.Y + 2] != 1:
            tempArray.append(Node(node.X, node.Y + 2,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X][node.Y + 1])

        while len(tempArray) > 0:
            tempNode = tempArray.pop()
            listOfNodes.append(tempNode)
            listOfWeights.append(tempWeightIndexesArray.pop())

def aStar(mazeForA, startX, startY, endX, endY):
    maze = mazeForA
    startX = int(startX)*2
    startY = int(startY)*2
    endX = int(endX)*2
    endY = int(endY)*2

    # list of Nodes (with coordinates)
    listOfNodes = []
    # Nodes weights
    listOfWeights = []

    listOfNodes.append(Node(startX, startY, None))
    listOfWeights.append(0)

    # randomize weights for fields
    newGrid, visited = randomizeWeights(maze)

    startNode = None
    path = []
    while len(listOfNodes) > 0:
        minIndex = listOfWeights.index(min(listOfWeights))
        node = listOfNodes[minIndex]
        weightNode = listOfWeights[minIndex]
        newGrid[node.X][node.Y] = weightNode 
        listOfWeights[minIndex] = sys.maxsize

        startNode = Node(node.X, node.Y, startNode)
        visited[node.X][node.Y] = 1

        # if we find endpoint
        if node.X == endX and node.Y == endY:
            path = findPathUcs(node)
            return path
        
        heuristicType = "m"
        tempArray = []
        tempWeightIndexesArray = []
        if node.X - 2 >= 0 and visited[node.X - 2][node.Y] != 1:
            tempArray.append(Node(node.X - 2, node.Y,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X - 1][node.Y] + heuristic((node.X - 1,node.Y),(endX,endY),heuristicType))
        if node.Y - 2 >= 0 and visited[node.X][node.Y - 2] != 1:
            tempArray.append(Node(node.X, node.Y - 2,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X][node.Y - 1] + heuristic((node.X,node.Y - 1),(endX,endY),heuristicType))
        if node.X + 2 < len(newGrid) and visited[node.X + 2][node.Y] != 1:
            tempArray.append(Node(node.X + 2, node.Y,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X + 1][node.Y] + heuristic((node.X + 1,node.Y),(endX,endY),heuristicType))
        if node.Y + 2 < len(newGrid[0]) and visited[node.X][node.Y + 2] != 1:
            tempArray.append(Node(node.X, node.Y + 2,node))
            tempWeightIndexesArray.append(weightNode + newGrid[node.X][node.Y + 1] + heuristic((node.X,node.Y + 1),(endX,endY),heuristicType))

        while len(tempArray) > 0:
            tempNode = tempArray.pop()
            listOfNodes.append(tempNode)
            listOfWeights.append(tempWeightIndexesArray.pop())
        



class Node:
    def __init__(self, x, y, newNode = None):
        self.X = x
        self.Y = y
        self.Node = newNode
    def name(self,new):
        if self.Node != None:
          new.append(self.Node)
          return self.name(new)
        else:
            return new

def randomizeWeights(grid):
    newGrid = []
    visitedGrid = []
    for i in range(len(grid)*2 - 1):
        row = []
        addRow = []
        for j in range(len(grid[0])*2 - 1):
            if (i % 2 == 0) and (j % 2 == 0):
                row.append(grid[int(i/2)][int(j/2)])
                if(grid[int(i/2)][int(j/2)] == 1):
                    addRow.append(0)
                else:
                    addRow.append(1)
            elif(i % 2 != 0) and (j % 2 != 0):
                row.append(0)
                addRow.append(1)
            else:
                row.append(random.randint(2,9))
                addRow.append(0)
        newGrid.append(row)
        visitedGrid.append(addRow)

    return newGrid, visitedGrid

def findPathUcs(node):
    queue = []
    while(node != None):
        queue.append((node.X/2,node.Y/2))
        node = node.Node
    return queue

def heuristic(a, b, typeH):
    manhattan = abs(a[0] - b[0]) + abs(a[1] - b[1])
    euclide = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
    euclideSquare = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    if(typeH == "m"):
        cost = manhattan
    elif(typeH == "e"):
        cost = euclide
    elif(typeH == "es"):
        cost = euclideSquare
    return cost

def pathThroughDots(maze, listOfDots):
    pathes = []
    for i in range(len(listOfDots) - 1):
        queueAStar = aStar(maze, listOfDots[i][0], listOfDots[i][1], listOfDots[i + 1][0], listOfDots[i + 1][1])
        queueAStar.reverse()
        pathes.append(queueAStar)
    path = []
    for row in pathes:
        for item in row:
            path.append(item)
    return path

#метод для зображення шляху на полі
def drawPath(self, path, screen, wholeGrid):
    for i in range(len(path)):
        color = RED
        pygame.draw.rect(screen, color, pygame.Rect(path[i][1]*32 + 9, path[i][0]*32 + 9, 16, 16))

#reconstruct path to DFS algorithm 
def reconstructPath(maze,x,y):
    stop = True
    envHight = len(maze)
    envWidth = len(maze[0])
    Dir = [[-1, 0], [0, -1], [1, 0],[0, 1]]
    queue = []
    queue.append((x,y))

    valid = False

    newArr = []
    for i in range(len(maze)):
        newArr.append([])
        for j in range(len(maze[i])):
            if(maze[i][j] == True):
                newArr[-1].append(0)
            else:
                newArr[-1].append(maze[i][j])

            if maze[i][j] == 2:
                valid = True
    
    maze = newArr
    if valid:
        while stop:
            p = queue[len(queue)-1]
            for item in range(4):
                # using the direction array
                a = p[0] + Dir[item][0]
                b = p[1] + Dir[item][1]

                # not blocked and valid
                if(a >= 0 and b >= 0 and a < envHight and b < envWidth and maze[a][b] > 0 and maze[a][b] < maze[p[0]][p[1]]) :           
                    queue.append((a, b))
                    break
            if(maze[p[0]][p[1]]==2):
                stop = False
        return (queue)
    else:
        return (queue)


#BFS
def findPathBFS(maze,startX,startY,endX,endY):
    startX = int(startX)
    startY = int(startY)
    endX = int(endX)
    endY = int(endY)

    queue = []
    queue.append((startX,startY))
    envHight = len(maze)
    envWidth = len(maze[0])
    Dir = [[-1, 0], [0, -1], [1, 0],[0, 1]]
    weight = 1

    visited = []
    for i in range(len(maze)):
        visited.append([])
        for j in range(len(maze[i])):
            if(maze[i][j]!=0):
                visited[-1].append(0)
            else:
                visited[-1].append(True)

    visited[startX][startY] = 1
    oldCount = 1
    newCount = 0
    while len(queue)>0:
        
        p = queue[0]
        queue.pop(0)

        if (p[0] == endX and p[1]== endY):
            queue = reconstructPath(visited,p[0],p[1])
            return queue
  
        for item in range(4):
            # using the direction array
            a = p[0] + Dir[item][0]
            b = p[1] + Dir[item][1]

            # not blocked and valid
            if(a >= 0 and b >= 0 and a < envHight and b < envWidth and visited[a][b] == 0 and visited[a][b] != True) :       
                visited[a][b]= weight + 1   
                queue.append((a, b))
                newCount += 1
        
        oldCount -= 1
        if(oldCount <= 0):
            oldCount = newCount
            newCount = 0
            weight+=1
    
    return queue
        
            


