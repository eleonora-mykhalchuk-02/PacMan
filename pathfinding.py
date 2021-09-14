from enemies import *
from game import*

#задаємо розширення екрану в залежності від розмірів ігроового поля
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 640

def newGrid():
    addGrid = []
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            row.append(0)
        addGrid.append(row)
    return addGrid


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

def bfs(startI, startJ, endI, endJ):
    addGrid = newGrid()
    addGrid[startI][startJ] = 1
    k = 1
    while addGrid[endI][endJ] == 0:
        stepBfs(k, addGrid)
        k += 1
    path = findPathBfs(addGrid, endI, endJ)
    return path

pathDfs = []

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

def ucs():
    gridForUcs = []
    for i in range(0, len(grid)*2 - 1):
        row = []
        for j in range(0, len(grid[0])*2 - 1):
            if (i % 2 == 0) and (j % 2 == 0):
                row.append(grid[int(i/2)][int(j/2)])
            elif(i % 2 != 0) and (j % 2 != 0):
                row.append(0)
            else:
                row.append(random.randint(2,9))
        gridForUcs.append(row)
    gridForUcs

def drawPath(path, screen):
        for point in path:
            pygame.draw.rect(screen, RED, pygame.Rect(point[1]*32 + 9, point[0]*32 + 9, 16, 16))
            


