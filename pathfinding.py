from enemies import *
from game import*
import sys

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREENWIDTH = 672
SCREENHEIGHT = 640

#створення допоміжного поля для алгоритму BFS
def newGrid():
    addGrid = []
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            row.append(0)
        addGrid.append(row)
    return addGrid

#метод реалізації "кроку" для пошуку в ширину
def stepBfs(k, addGrid):
    for i in range(len(addGrid)):
        for j in range(len(addGrid[i])):
            if addGrid[i][j] == k:
                if i>0 and addGrid[i-1][j] == 0 and grid[i-1][j] == 1:
                    addGrid[i-1][j] = k + 1
                if j>0 and addGrid[i][j-1] == 0 and grid[i][j-1] == 1:
                    addGrid[i][j-1] = k + 1
                if i<len(addGrid)-1 and addGrid[i+1][j] == 0 and grid[i+1][j] == 1:
                    addGrid[i+1][j] = k + 1
                if j<len(addGrid[i])-1 and addGrid[i][j+1] == 0 and grid[i][j+1] == 1:
                    addGrid[i][j+1] = k + 1

#метод реалізації покрокового проходження поля для пошуку в ширину
def findPathBfs(addGrid, i, j):
    k = addGrid[i][j]
    path = [(i, j)]
    while k > 1:
        if i > 0 and addGrid[i - 1][j] == k-1:
            i, j = i-1, j
            path.append((i, j))
            k-=1
        elif j > 0 and addGrid[i][j - 1] == k-1:
            i, j = i, j-1
            path.append((i, j))
            k-=1
        elif i < len(addGrid) - 1 and addGrid[i + 1][j] == k-1:
            i, j = i+1, j
            path.append((i, j))
            k-=1
        elif j < len(addGrid[i]) - 1 and addGrid[i][j + 1] == k-1:
            i, j = i, j+1
            path.append((i, j))
            k -= 1
    return path

#метод реалізації пошуку в ширину
def bfs(startI, startJ, endI, endJ):
    addGrid = newGrid()
    addGrid[startI][startJ] = 1
    k = 1
    while addGrid[endI][endJ] == 0:
        stepBfs(k, addGrid)
        k += 1
    path = findPathBfs(addGrid, endI, endJ)
    return path

#створення списку для точок шляху
pathDfs = []
#метод реалізації пошуку шляху в глибину
def pathForDfs(startI, startJ, endI, endJ):
    gridForDfs = []
    for rows in grid:
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
            print('path:', path)
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

class Node:
    def __init__(self, x, y, newNode = None):
        self.X = x
        self.Y = y
        self.Node = newNode
    def name(self,new):
        if self.Node != None:
          new.append(self.Node)
          print(self.X," ", self.Y)
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

#метод для зображення шляху на полі
def drawPath(path, screen):
        for point in path:
            pygame.draw.rect(screen, RED, pygame.Rect(point[1]*32 + 9, point[0]*32 + 9, 16, 16))
            


